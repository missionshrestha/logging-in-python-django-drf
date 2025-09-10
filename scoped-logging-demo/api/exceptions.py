# api/exceptions.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from scoped_logging.context import trace_id_var

def traced_exception_handler(exc, context):
    # Let DRF build the default response first (includes nice validation structure, etc.)
    response = exception_handler(exc, context)

    trace_id = trace_id_var.get() or "-"
    if response is None:
        # Non-DRF exceptions
        data = {
            "error": "internal_server_error",
            "message": str(exc) or "Internal Server Error",
            "trace_id": trace_id,
        }
        return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # DRF-aware exceptions
    data = {
        "error": getattr(exc, "default_code", "error"),
        "detail": response.data,
        "trace_id": trace_id,
    }
    response.data = data
    # also surface header (middleware already does this, but harmless)
    response["X-Trace-Id"] = trace_id
    return response
