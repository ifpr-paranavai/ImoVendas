from django.urls import path
from .views import ImovelCreate, ImovelList

urlpatterns = [
    path('criar/imovel/', ImovelCreate.as_view(template_name='cadastros/imovel-form.html'), name='criar-imovel'),
    path('listar/imovel/', ImovelList.as_view(template_name='cadastros/imovel-list.html'), name='listar-imovel'),
]
