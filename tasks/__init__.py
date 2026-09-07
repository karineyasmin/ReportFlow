"""
Celery asynchronous task definitions and worker package.
"""

from app.tasks.report_tasks import generate_sales_report
from app.tasks.worker import celery_app

__all__ = [
    "celery_app",
    "generate_sales_report",
]
