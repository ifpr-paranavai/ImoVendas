from django.urls import path
from .views import ImovelBoost, ImovelView, Index


urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('ver/imovel/<pk>/', ImovelView.as_view(), name='imovel-view'),
    path('destacar/<pk>/', ImovelBoost.as_view(), name='imovel-boost'),
]