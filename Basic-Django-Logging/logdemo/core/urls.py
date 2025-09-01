from django.urls import path
from .views import test_view

urlpatterns = [
    path('test-logging/', test_view, name='test-logging'),
]
