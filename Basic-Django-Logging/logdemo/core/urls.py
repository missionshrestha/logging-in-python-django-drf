from django.urls import path
from .views import test_core

urlpatterns = [
    path('core-log/', test_core, name='core-log'),
]
