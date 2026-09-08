"""
Core module initialization.

This module aggregates and exposes central system utilities,
such as application settings and the custom colored logger instance,
making them easily accessible from a single import point.
"""

from app.core.config import settings
from app.core.logger import logger

__all__ = [
    "settings",
    "logger",
]
