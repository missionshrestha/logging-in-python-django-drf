# scoped-logging-demo/api/urls.py
from django.urls import path
from .views import BoomView, EchoView, WorkView

urlpatterns = [
    path("v1/echo/", EchoView.as_view(), name="echo"),
    path("v1/work/", WorkView.as_view(), name="work"),
    path("v1/boom/", BoomView.as_view(), name="boom"),
]
