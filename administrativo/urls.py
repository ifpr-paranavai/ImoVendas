from django.urls import path
from .views import Adm, aprovarImovel, rejeitarImovel


urlpatterns = [
    path('administrativo/', Adm.as_view(), name='adm'),
    path('administrativo/aprovar/<int:pk>/<int:historico_pk>/<int:destaque>/', aprovarImovel, name='aprovar-imovel'),
    path('administrativo/rejeitar/<int:historico_pk>/', rejeitarImovel, name='rejeitar-imovel'),
]