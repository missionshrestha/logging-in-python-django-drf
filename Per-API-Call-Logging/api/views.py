from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def echo(request):
    request.logger.info("VALIDATING_INPUT")
    data = request.data or {}

    if "fail" in data:
        request.logger.warning("CLIENT_REQUESTED_FAILURE", extra={"reason": "fail flag present"})
        return Response({"detail": "You asked me to fail."}, status=status.HTTP_400_BAD_REQUEST)

    request.logger.info("CALLING_DOWNSTREAM_SERVICE", extra={"service": "payment", "timeout_ms": 500})
    # ... call downstream, do work ...
    request.logger.info("DOWNSTREAM_SERVICE_OK", extra={"service": "payment"})

    result = {"echo": data, "request_id": getattr(request, "_request_id", None)}
    request.logger.info("RETURNING_RESPONSE")
    return Response(result, status=status.HTTP_200_OK)
