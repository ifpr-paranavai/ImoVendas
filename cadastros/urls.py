from django.urls import path
from .views import ImovelCreate, ImovelList, ImovelSearch, imovelFinish

urlpatterns = [
    path('criar/imovel/', ImovelCreate.as_view(template_name='cadastros/imovel-form.html'), name='criar-imovel'),
    path('listar/imovel/', ImovelList.as_view(template_name='cadastros/imovel-list.html'), name='listar-imovel'),
    path('negociar/imovel/<int:pk>/', imovelFinish, name='negociar-imovel'),
    path('buscar/imovel/', ImovelSearch.as_view(), name='buscar-imovel'),
]
