from .models import Visitor
import user_agents

EXCLUDE_PATH_PREFIXES = ("/static/", "/media/", "/admin/", "/api/", "/favicon.ico")

class VisitorTrackingMiddleware:
    """
    Create a Visitor record only for top-level navigations (page loads / refreshes).
    This runs BEFORE get_response so the visitor is recorded as soon as the request
    arrives (but only for document navigations, not for XHR/fetch requests).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def _client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR") or ""

    def _is_bot(self, ua_string):
        try:
            ua = user_agents.parse(ua_string)
            return getattr(ua, "is_bot", False)
        except Exception:
            return False

    def _looks_like_navigation(self, request):
        """
        Heuristics for top-level navigation:
        - Sec-Fetch-Mode == "navigate" (modern browsers on navigations & refresh)
        - Sec-Fetch-Dest == "document"
        - OR Accept header includes "text/html" and it's not XHR
        """
        headers = request.headers
        # XHR quick skip
        if headers.get("x-requested-with", "").lower() == "xmlhttprequest":
            return False

        sec_fetch_mode = headers.get("sec-fetch-mode", "").lower()
        sec_fetch_dest = headers.get("sec-fetch-dest", "").lower()
        accept = headers.get("accept", "").lower()

        if sec_fetch_mode == "navigate":
            return True
        if sec_fetch_dest == "document":
            return True
        # Fallback: page loads usually accept HTML
        if "text/html" in accept:
            return True

        return False

    def __call__(self, request):
        # Only GET navigations
        if request.method != "GET":
            return self.get_response(request)

        path = (request.path or "").lower()
        # Skip static, media, admin, api and favicon
        if any(path.startswith(p) for p in EXCLUDE_PATH_PREFIXES):
            return self.get_response(request)

        # Only when it looks like a top-level navigation
        if not self._looks_like_navigation(request):
            return self.get_response(request)

        # Don't track bots
        ua_string = request.META.get("HTTP_USER_AGENT", "")
        if self._is_bot(ua_string):
            return self.get_response(request)

        # Get IP and create visitor BEFORE response (best-effort)
        ip = self._client_ip(request)
        try:
            Visitor.objects.create(ip_address=ip, user_agent=ua_string)
        except Exception:
            # Fail silently; we don't want DB errors to break page loads
            pass

        # Continue processing
        return self.get_response(request)
