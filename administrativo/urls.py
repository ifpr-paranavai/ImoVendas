from django.urls import path
from .views import Adm, Movimentacoes, RotinaImovel, Usuarios, aprovarImovel, rejeitarImovel


urlpatterns = [
    path('administrativo/', Adm.as_view(), name='adm'),
    path('administrativo/movimentacoes', Movimentacoes.as_view(), name='movs'),
    path('administrativo/usuarios', Usuarios.as_view(), name='usuarios'),
    path('administrativo/aprovar/<int:pk>/<int:historico_pk>/<int:destaque>/', aprovarImovel, name='aprovar-imovel'),
    path('administrativo/rejeitar/<int:historico_pk>/', rejeitarImovel, name='rejeitar-imovel'),
    path('administrativo/rotinas', RotinaImovel.as_view(), name='rotinas'),
]