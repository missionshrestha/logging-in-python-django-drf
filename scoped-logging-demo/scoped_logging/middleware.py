# scoped_logging/middleware.py
from __future__ import annotations
from typing import Callable
from pathlib import Path
from django.http import HttpRequest, HttpResponse, HttpResponseServerError
from django.utils.deprecation import MiddlewareMixin
from .context import start_scope, end_scope, get_logger, safe_filename, trace_id_var

class ScopedRequestLoggingMiddleware(MiddlewareMixin):
    def __init__(self, get_response: Callable):
        super().__init__(get_response)
        self.get_response = get_response
        self.base_dir = Path("logs")

    def __call__(self, request: HttpRequest) -> HttpResponse:
        label = f"{request.method}_{safe_filename((request.path or '/').strip('/')) or 'root'}"
        start_scope("request", self.base_dir, label, base_logger_name="app", reuse_if_exists=True)

        logger = get_logger("request")
        logger.info(f"➡️ Request start: {request.method} {request.get_full_path()}")

        response: HttpResponse | None = None
        try:
            response = self.get_response(request)
            logger.info("✅ Request end")
        except Exception:
            # We still log and return a 500 so we can attach the trace header
            logger.exception("💥 Unhandled exception during request")
            response = HttpResponseServerError()  # minimal; swap for custom JSON if you prefer
        finally:
            # Always surface correlation id on the response we are returning
            if response is not None:
                response["X-Trace-Id"] = trace_id_var.get() or "-"
            # Tear down the file handler and (optionally) log the file path
            logfile = end_scope("app")
            if logfile:
                logger.info(f"🗂️ Request log file: {logfile}")

        return response
