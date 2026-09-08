"""
Background asynchronous tasks for report generation.
"""

import time
from celery import Task
from typing import Any

from app.core import logger
from app.services.report_generator import (
    generate_sales_dataframe,
    export_dataframe_to_csv,
)
from app.tasks.worker import celery_app


@celery_app.task(bind=True)
def generate_sales_report(self: Task, total_records: int = 10000) -> dict[str, Any]:
    """
    Orchestrates the background export pipeline:
    delegates dataset generation and file writing to dedicated service layers.
    """

    task_id = self.request.id
    logger.info(
        f"Task [{task_id}] - Initiating export pipeline for {total_records} records."
    )

    # Simulate heavy processing delay
    time.sleep(5)

    # 1. Fetch/build dataset
    df = generate_sales_dataframe(total_records)

    # 2. Export to disk
    file_path = export_dataframe_to_csv(df, filename=f"report_{task_id}.csv")
    logger.info(f"Task [{task_id}] - Export completed successfully: {file_path}")

    return {
        "status": "COMPLETED",
        "task_id": task_id,
        "records_processed": total_records,
        "file_path": file_path,
        "format": "csv",
    }
