from datetime import date, datetime, timedelta
from braces.views import GroupRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView

from cadastros.models import Foto, Movimentacao, Imovel


class Adm(GroupRequiredMixin, ListView):
    group_required = u"Administrador"
    model = Imovel
    template_name = "administrativo/index.html"

    def get_queryset(self):
        lista = []

        movimentacoes = Movimentacao.objects.filter(pendente=True).select_related("imovel")

        if not movimentacoes.exists():
            return lista

        for mov in movimentacoes:
            imovel_foto = Foto.objects.filter(imovel=mov.imovel)[0],
            lista.append([
                mov,
                imovel_foto[0],
            ])

        return lista

class Movimentacoes(GroupRequiredMixin, ListView):
    group_required = u"Administrador"
    model = Movimentacao
    template_name = "administrativo/movs.html"

    def get_queryset(self):
        lista = []

        imoveis = Imovel.objects.all()

        for imovel in imoveis:
            movimentacoes = Movimentacao.objects.filter(imovel=imovel)
            lista.append([
                imovel,
                Foto.objects.filter(imovel=imovel)[0],
                movimentacoes,
            ])

        return lista

class Usuarios(GroupRequiredMixin, ListView):
    group_required = u"Administrador"
    model = User
    template_name = "administrativo/users.html"



def temPermissao(request):
    user = request.user
    if user:
        return user.groups.filter(name="Administrador").exists()

    return False


def aprovarImovel(request, pk=None, historico_pk=None, destaque=False):
    if temPermissao(request):
        imovel = Imovel.objects.get(usuario=request.user, pk=pk)
        historico_atual = Movimentacao.objects.get(pk=historico_pk)
        
        if imovel and historico_atual and historico_atual.pendente:
            if destaque and imovel.publicado:
                imovel.destacado = True
            else:
                imovel.publicado = True
                imovel.expira_em = date.today() + timedelta(days=30)

            imovel.save()

            historico_atual.pendente = False
            historico_atual.save()

            historico = Movimentacao.objects.create(imovel=imovel, movimentado_por=request.user)
            historico.pendente = False
            historico.motivo = f"{historico_atual.motivo} (Aprovado)"
            historico.save()
            
            return redirect("adm")


def rejeitarImovel(request, historico_pk=None):
    if temPermissao(request):
        historico_atual = Movimentacao.objects.get(pk=historico_pk)
        if historico_atual and historico_atual.pendente:
            historico_atual.pendente = False
            historico_atual.save()

            historico = Movimentacao.objects.create(imovel=historico_atual.imovel, movimentado_por=request.user)
            historico.pendente = False
            historico.motivo = f"{historico_atual.motivo} (Rejeitado)"
            historico.save()
            return redirect("adm")
        
            
            
class RotinaImovel(GroupRequiredMixin, TemplateView):
    group_required = u"Administrador"
    template_name = "administrativo/rotina.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        imoveis_expirados = Imovel.objects.filter(expira_em__lt=datetime.now())
        count = 0

        for imovel in imoveis_expirados:
            count+=1
            imovel.publicado = False
            imovel.save()

            historico = Movimentacao.objects.create(imovel=imovel, movimentado_por=self.request.user)
            historico.motivo = "Imóvel expirado"
            historico.pendente = False
            historico.save()

        context["contagem"] = count
        return context
