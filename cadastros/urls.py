from django.urls import path
from .views import ImovelCreate

urlpatterns = [
    path('criar/imovel/', ImovelCreate.as_view(template_name='cadastros/imovel-form.html'), name='criar-imovel'),
]
