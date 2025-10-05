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
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)
        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict access to the chat app outside working hours.
    Allowed time: 06:00 - 21:00 (6AM - 9PM).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden(
                "⛔ Access restricted: Chats are only available between 6AM and 9PM."
            )
        return self.get_response(request)


class OffensiveLanguageMiddleware:
    """
    Middleware to rate-limit chat messages by IP.
    Restricts to 5 POST requests per minute per IP.
    """

    ip_request_log = defaultdict(list)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        client_ip = self.get_client_ip(request)

        if request.method == "POST" and "/messages" in request.path:
            now = datetime.now()
            window_start = now - timedelta(minutes=1)

            self.ip_request_log[client_ip] = [
                ts for ts in self.ip_request_log[client_ip] if ts > window_start
            ]

            if len(self.ip_request_log[client_ip]) >= 5:
                return HttpResponseForbidden(
                    "🚫 Rate limit exceeded: You can only send 5 messages per minute."
                )

            self.ip_request_log[client_ip].append(now)

        return self.get_response(request)

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR", "unknown")


class RolePermissionMiddleware:
    """
    Middleware to enforce role-based access for chats.
    Only users with role 'admin' or 'moderator' can access restricted endpoints.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define restricted paths (could also use regex for patterns)
        restricted_paths = ["/admin-only/", "/moderator-actions/"]

        if any(path in request.path for path in restricted_paths):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("❌ Access denied: You must log in.")

            if getattr(request.user, "role", None) not in ["admin", "moderator"]:
                return HttpResponseForbidden(
                    "🚫 Access denied: Only admins or moderators can perform this action."
                )

        return self.get_response(request)
