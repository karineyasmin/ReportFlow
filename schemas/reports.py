"""
Pydantic schemas for request and response validation.
"""

from typing import Any

from pydantic import BaseModel, Field


class ReportRequest(BaseModel):
    """Payload to trigger report generation."""

    total_records: int = Field(
        default=1000,
        ge=10,
        le=100000,
        description="Number of records to synthesize in the report.",
    )


class ReportAcceptedResponse(BaseModel):
    """Response returned upon successfully enqueuing the background task."""

    task_id: str
    status: str
    message: str


class ReportStatusResponse(BaseModel):
    """Response schema tracking Celery task execution status."""

    task_id: str
    status: str
    result: dict[str, Any] | None = None
    error: str | None = None
