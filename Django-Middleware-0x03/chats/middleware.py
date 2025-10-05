# chats/middleware.py
import logging
from datetime import datetime

# Configure logging to write to requests.log
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("requests.log")
formatter = logging.Formatter("%(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


class RequestLoggingMiddleware:
    """
    Middleware to log each request with timestamp, user, and request path.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Identify user
        user = request.user if request.user.is_authenticated else "Anonymous"

        # Log request
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        # Continue request cycle
        response = self.get_response(request)
        return response
