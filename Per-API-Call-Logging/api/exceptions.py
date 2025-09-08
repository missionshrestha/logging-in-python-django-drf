from rest_framework.views import exception_handler as drf_exception_handler

def custom_exception_handler(exc, context):
    """
    First let DRF produce the default response.
    Then log a compact error line into the per-request file (if available).
    """
    response = drf_exception_handler(exc, context)
    request = context.get("request")
    if request is not None and hasattr(request, "logger"):
        request.logger.error("DRF_EXCEPTION", extra={
            "exc_class": exc.__class__.__name__,
            "status_code": getattr(response, "status_code", None),
        })
    return response
