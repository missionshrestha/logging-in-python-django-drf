from django.urls import path
from .views import test_shop

urlpatterns = [
    path('shop-log/', test_shop, name='shop-log'),
]
