import logging
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden
from collections import defaultdict

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
                "⛔ Access restricted: Chats are only available between 6AM and 9PM."
            )

        # Otherwise continue request cycle
        return self.get_response(request)


class OffensiveLanguageMiddleware:
    """
    Middleware to rate-limit chat messages by IP.
    Restricts to 5 POST requests per minute per IP.
    """

    # Store request timestamps per IP
    ip_request_log = defaultdict(list)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        client_ip = self.get_client_ip(request)

        # Only rate-limit POST requests to message endpoints
        if request.method == "POST" and "/messages" in request.path:
            now = datetime.now()
            window_start = now - timedelta(minutes=1)

            # Clean old entries
            self.ip_request_log[client_ip] = [
                ts for ts in self.ip_request_log[client_ip] if ts > window_start
            ]

            # Check if limit exceeded
            if len(self.ip_request_log[client_ip]) >= 5:
                return HttpResponseForbidden(
                    "🚫 Rate limit exceeded: You can only send 5 messages per minute."
                )

            # Record this request timestamp
            self.ip_request_log[client_ip].append(now)

        return self.get_response(request)

    @staticmethod
    def get_client_ip(request):
        """Helper to extract client IP safely."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR", "unknown")
