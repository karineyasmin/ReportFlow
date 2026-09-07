"""
Celery worker configuration and application instance initialization.
"""

from celery import Celery
from app.core import settings

celery_app = Celery(
    "reportflow_tasks",
    broker=settings.CELERY_BROKER_URL,
    include=["app.tasks.report_tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezne="UTC",
    enable_utc=True,
    task_track_started=True,
)
