"""
API endpoints for dispatching and inspecting report generation tasks.
"""

import os
from typing import Any

from celery.result import AsyncResult
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse

from app.auth import require_role, verify_jwt_token
from app.core import logger
from app.schemas.reports import (
    ReportRequest,
    ReportAcceptedResponse,
    ReportStatusResponse,
)
from app.tasks import generate_sales_report

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.post(
    "",
    response_model=ReportAcceptedResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Enqueue a new report generation job",
)
def create_report(
    request: ReportRequest,
    user_payload: dict[str | Any] = Depends(require_role("report_admin")),
):
    """
    Enqueues the CSV generation task into Celery/Redis.
    Requires 'report_admin' role from Keycloak.
    """

    username = user_payload.get("preferred_username", "anonymous")
    logger.info(
        f"User '{username}' requested report generation ({request.total_records} records)."
    )

    # Dispatcher the task to the Celery broker asynchronously
    async_task = generate_sales_report.delay(total_records=request.total_records)

    return ReportAcceptedResponse(
        task_id=async_task.id,
        status="PENDING",
        message="Report generation has been queued successfully.",
    )


@router.get(
    "/{task_id}",
    response_model=ReportStatusResponse,
    summary="Inspect task execution state",
)
def get_report_status(task_id: str, _: dict[str, Any] = Depends(verify_jwt_token)):
    """
    Inspects Celery state for a specific task using its task_id.
    Requires a valid JWT token.
    """
    task_result = AsyncResult(task_id)

    if task_result.state == "PENDING":
        return ReportStatusResponse(task_id=task_id, status=task_result.state)

    if task_result.state == "STARTED":
        return ReportStatusResponse(task_id=task_id, status=task_result.state)

    if task_result.state == "SUCCESS":
        return ReportStatusResponse(
            task_id=task_id, status=task_result.state, result=task_result.result
        )

    if task_result.state == "FAILURE":
        return ReportStatusResponse(
            task_id=task_id, status=task_result.state, error=str(task_result.info)
        )

    return ReportStatusResponse(task_id=task_id, status=task_result.state)


@router.get("/{task_id}/download", summary="Download completed report file")
def download_report_file(task_id: str, _: dict[str, Any] = Depends(verify_jwt_token)):
    """
    Serves the output CSV file if the task completed successfully.
    """
    task_result = AsyncResult(task_id)

    if task_result.state != "SUCCESS":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Report is not ready yet. Current status: {task_result.state}",
        )

    result_data = task_result.result
    file_path = result_data.get("file_path")

    if not file_path or not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report file was not found on server storage.",
        )

    return FileResponse(
        path=file_path, media_type="text/csv", filename=os.path.basename(file_path)
    )
