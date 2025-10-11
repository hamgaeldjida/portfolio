# middleware.py
from datetime import timedelta
from django.utils import timezone
from .models import Visitor
import user_agents

class VisitorTrackingMiddleware:
    """
    Track a visitor only on "real" page views and only once per browser (cookie).
    - Only track GET requests
    - Skip XHR/AJAX requests
    - Skip static/media/admin/api/favicon paths
    - Skip known bots
    - Only create Visitor for HTML responses (status 200)
    - Set a cookie 'site_visited' to avoid repeated saves (default 30 days)
    """

    COOKIE_NAME = "site_visited"
    COOKIE_MAX_AGE = 30 * 24 * 60 * 60  # 30 days in seconds
    EXCLUDE_PATH_PREFIXES = ("/static/", "/media/", "/admin/", "/api/", "/favicon.ico")

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Quick rejects before doing any work
        if request.method != "GET":
            return self.get_response(request)

        # Skip AJAX/XHR (common for API calls and frontend fetches)
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return self.get_response(request)

        # Skip obvious non-page paths
        path = (request.path or "").lower()
        if path.startswith(self.EXCLUDE_PATH_PREFIXES):
            return self.get_response(request)

        # If cookie exists, we've already recorded this visitor recently
        if request.COOKIES.get(self.COOKIE_NAME):
            return self.get_response(request)

        # Let Django process the request first (we want response content-type/status)
        response = self.get_response(request)

        # Only track successful HTML page responses
        content_type = response.get("Content-Type", "")
        if response.status_code == 200 and "text/html" in content_type:
            # Get client IP (best-effort)
            x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
            if x_forwarded_for:
                ip = x_forwarded_for.split(",")[0].strip()
            else:
                ip = request.META.get("REMOTE_ADDR") or ""

            user_agent_str = request.META.get("HTTP_USER_AGENT", "")

            # Skip bots
            try:
                ua = user_agents.parse(user_agent_str)
                if getattr(ua, "is_bot", False):
                    return response
            except Exception:
                # If user_agents parsing fails, continue and just store raw UA
                pass

            # Create visitor record
            try:
                Visitor.objects.create(
                    ip_address=ip,
                    user_agent=user_agent_str
                )
            except Exception:
                # Fail silently — we don't want the whole request to crash on DB issues.
                pass

            # Set a cookie so this browser won't be recorded again for COOKIE_MAX_AGE seconds
            response.set_cookie(
                self.COOKIE_NAME,
                "1",
                max_age=self.COOKIE_MAX_AGE,
                httponly=True,
                samesite="Lax",
            )

        return response
