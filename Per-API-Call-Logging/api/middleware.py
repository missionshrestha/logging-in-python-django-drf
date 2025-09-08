import logging
import uuid
from datetime import datetime
from django.conf import settings
from pathlib import Path

class RequestLoggerAdapter(logging.LoggerAdapter):
    """Injects request_id/method/path into every log call automatically."""
    def process(self, msg, kwargs):
        extra = kwargs.get("extra", {})
        extra.setdefault("request_id", self.extra.get("request_id"))
        extra.setdefault("method", self.extra.get("method"))
        extra.setdefault("path", self.extra.get("path"))
        kwargs["extra"] = extra
        return msg, kwargs

class PerRequestLoggingMiddleware:
    """
    Creates one file per API call. Each file captures everything you log
    with request.logger.

    File name pattern:
      logs/requests/YYYYMMDD/HHMMSS_<request_id>.log
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1) Correlation ID (trust upstream X-Request-ID if present)
        header_name = getattr(settings, "REQUEST_ID_HEADER", "HTTP_X_REQUEST_ID")
        request_id = request.META.get(header_name) or uuid.uuid4().hex

        # 2) Build file path (partition by date)
        now = datetime.utcnow()
        date_dir = Path(settings.REQUEST_LOG_DIR) / now.strftime("%Y%m%d")
        date_dir.mkdir(parents=True, exist_ok=True)
        filename = date_dir / f"{now.strftime('%H%M%S')}_{request_id}.log"

        # 3) Create a dedicated logger for this request
        logger = logging.getLogger(f"request.{request_id}")
        logger.setLevel(logging.INFO)
        logger.propagate = False  # do not duplicate into app-wide handlers

        handler = logging.FileHandler(filename)
        formatter = logging.Formatter(
            fmt='%(asctime)s %(levelname)s %(name)s %(message)s '
                'request_id=%(request_id)s method=%(method)s path=%(path)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # 4) Attach convenient adapter to the request
        request.logger = RequestLoggerAdapter(logger, {
            "request_id": request_id, "method": request.method, "path": request.path
        })
        request._per_request_log_handler = handler
        request._per_request_logger = logger
        request._per_request_logfile = str(filename)
        request._request_id = request_id

        # 5) Log entry line
        request.logger.info("START", extra={"client_ip": request.META.get("REMOTE_ADDR")})

        try:
            # 6) Downstream view
            response = self.get_response(request)
        except Exception:
            # 7) Log unhandled exceptions (with stack trace)
            request.logger.exception("UNHANDLED_EXCEPTION")
            raise
        finally:
            # 8) Always log END + status and add response header
            try:
                status_code = getattr(response, "status_code", None)
                request.logger.info("END", extra={"status_code": status_code})
            except Exception:
                pass

            try:
                if hasattr(response, "__setitem__"):
                    response[settings.REQUEST_ID_RESPONSE_HEADER] = request_id
            except Exception:
                pass

            # 9) Clean up the handler (avoid fd leaks)
            try:
                request._per_request_logger.removeHandler(request._per_request_log_handler)
                request._per_request_log_handler.close()
            except Exception:
                pass

        return response
