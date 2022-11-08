from django.urls import path
from .views import ImovelPagar, ImovelView, Index


urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('ver/imovel/<pk>/', ImovelView.as_view(), name='imovel-view'),
    path('destacar/<pk>/', ImovelPagar.as_view(modo="destacar"), name='imovel-boost'),
    path('renovar/<pk>/', ImovelPagar.as_view(modo="renovar"), name='imovel-renew'),
]