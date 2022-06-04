from django.urls import path
from .views import ImovelCreate

urlpatterns = [
    path('cadastrar/imovel/', ImovelCreate.as_view(template_name='cadastros/imovel-form.html'), name='cadastro-imovel'),
]
