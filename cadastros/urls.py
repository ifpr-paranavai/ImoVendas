from django.urls import path
from .views import ImovelCreate, ImovelList, ImovelSearch, imovelDelete

urlpatterns = [
    path('criar/imovel/', ImovelCreate.as_view(template_name='cadastros/imovel-form.html'), name='criar-imovel'),
    path('listar/imovel/', ImovelList.as_view(template_name='cadastros/imovel-list.html'), name='listar-imovel'),
    path('excluir/imovel/<int:pk>/', imovelDelete, name='excluir-imovel'),
    path('buscar/imovel/', ImovelSearch.as_view(), name='buscar-imovel'),
]
