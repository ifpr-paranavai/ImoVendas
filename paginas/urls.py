from django.urls import path
from .views import ImovelView, Index


urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('imovel/<pk>/', ImovelView.as_view(), name='imovel-view'),
]