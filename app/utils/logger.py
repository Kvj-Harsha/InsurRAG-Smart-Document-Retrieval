import logging
import sys
import json # Added import for json
from typing import Any, Dict

from app.utils.config import settings # Import settings from our config file

class StructuredFormatter(logging.Formatter):
    """
    A custom logging formatter that outputs logs as JSON,
    useful for structured logging and easier parsing by log aggregation systems.
    """
    def format(self, record: logging.LogRecord) -> str:
        log_record: Dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
            "pathname": record.pathname,
            "lineno": record.lineno,
            "process": record.process,
            "thread": record.thread,
        }

        # Add any extra attributes passed to the log record
        if hasattr(record, 'extra_data') and isinstance(record.extra_data, dict):
            log_record.update(record.extra_data)

        # If an exception is present, add its information
        if record.exc_info:
            log_record["exc_info"] = self.formatException(record.exc_info)
        if record.stack_info:
            log_record["stack_info"] = self.formatStack(record.stack_info)

        return_json = {}
        # Filter out empty or None values for cleaner logs
        for key, value in log_record.items():
            if value is not None and value != "":
                return_json[key] = value

        return json.dumps(return_json)

# Initialize a default logger
def setup_logging():
    """
    Sets up the application-wide logging configuration.
    Uses a StructuredFormatter if LOG_FORMAT is 'json', otherwise a simple console formatter.
    """
    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.LOG_LEVEL)

    # Clear existing handlers to prevent duplicate logs if setup_logging is called multiple times
    if root_logger.handlers:
        for handler in root_logger.handlers:
            root_logger.removeHandler(handler)

    # Create a console handler
    console_handler = logging.StreamHandler(sys.stdout)

    if settings.LOG_FORMAT == "json":
        formatter = StructuredFormatter(datefmt="%Y-%m-%dT%H:%M:%S%z")
    else:
        # Default console formatter for development
        formatter = logging.Formatter(
            "%(levelname)s:     %(asctime)s - %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Suppress verbose logs from external libraries if not in debug mode
    if not settings.DEBUG:
        logging.getLogger("uvicorn").setLevel(logging.INFO)
        logging.getLogger("uvicorn.access").setLevel(logging.INFO)
        logging.getLogger("httpx").setLevel(logging.WARNING) # Suppress httpx connection pool info
        logging.getLogger("weaviate").setLevel(logging.WARNING) # Suppress Weaviate client info

# Ensure logging is set up when this module is imported
# This makes sure that any module importing logger.py gets the configured logger
setup_logging()

# You can get a logger instance for specific modules like this:
# from app.utils.logger import logger
# logger = logging.getLogger(__name__)
# logger.info("This is an info message from my_module", extra={"user_id": "123"})
