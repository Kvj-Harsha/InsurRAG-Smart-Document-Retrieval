# test_logging.py
import logging
from app.utils.config import settings # Ensure config is imported first
from app.utils.logger import setup_logging # Import to trigger setup

# Get a logger instance for this specific module
logger = logging.getLogger(__name__)

def run_log_tests():
    print(f"--- Testing Logging (LOG_FORMAT: {settings.LOG_FORMAT}, LOG_LEVEL: {settings.LOG_LEVEL}) ---")
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message with extra data.", extra={"user_id": "abc", "transaction_id": "xyz"})
    logger.error("This is an error message with an exception.", exc_info=True)
    try:
        1 / 0
    except ZeroDivisionError:
        logger.critical("Critical error: Division by zero occurred!", exc_info=True)

if __name__ == "__main__":
    # Test with default settings (console format)
    print("\n--- Testing with default console format ---")
    settings.LOG_FORMAT = "console"
    settings.LOG_LEVEL = "DEBUG"
    setup_logging() # Re-setup logging with new format
    run_log_tests()

    # Test with JSON format
    print("\n--- Testing with JSON format ---")
    settings.LOG_FORMAT = "json"
    settings.LOG_LEVEL = "INFO" # Only info and above will show
    setup_logging() # Re-setup logging with new format
    run_log_tests()