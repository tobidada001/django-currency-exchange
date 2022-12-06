from . import views
from django.urls import path

urlpatterns = [
    path('', views.ExchangeView.as_view(), name = 'exchange'),
    path('price/', views.CryptoPriceView.as_view(), name = 'price')
]
