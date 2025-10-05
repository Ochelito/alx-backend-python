import logging
from datetime import datetime
from django.http import HttpResponseForbidden

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


class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict access to the chat app outside working hours.
    Allowed time: 06:00 - 21:00 (6AM - 9PM).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        # Block access if time is outside allowed range
        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden(
                " Access restricted: Chats are only available between 6AM and 9PM."
            )

        # Otherwise continue request cycle
        return self.get_response(request)
