# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from scoped_logging.context import get_logger
from scoped_logging.decorators import function_log_scope
from .services import greet
import time  # ⬅️ switched from asyncio to time.sleep for the demo

class EchoView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []  # keep demos simple

    def get(self, request):
        logger = get_logger(__name__)
        logger.info("EchoView.get: start")
        name = request.query_params.get("name", "world")
        out = greet(name, headers=request.headers)
        logger.info("EchoView.get: preparing response")
        return Response({"message": out}, status=status.HTTP_200_OK)

class WorkView(APIView):
    # Disable auth/CSRF for simple curl testing so the view actually runs.
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):  # ⬅️ sync now
        logger = get_logger(__name__)
        logger.info("WorkView.post: start (sync)")
        payload = request.data
        with function_log_scope("rebuild-index"):
            logger.info("WorkView.post: inside function scope; keys=%s", list(payload.keys()))
            time.sleep(0.02)  # fake work (sync)
        logger.info("WorkView.post: end")
        return Response({"status": "ok"})

class BoomView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        raise RuntimeError("boom")
