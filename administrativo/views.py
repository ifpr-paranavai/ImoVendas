from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from django.views.generic.list import ListView
from braces.views import GroupRequiredMixin
from cadastros.models import Foto, Historico, Imovel


class Adm(ListView, GroupRequiredMixin):
    model = Imovel
    group_required = "Administrador"
    template_name = "administrativo/index.html"

    def get_queryset(self):
        lista = []

        imoveis = Imovel.objects.all()
        movimentacoes = Historico.objects.filter(pendente=True)

        if len(movimentacoes) == 0:
            return lista

        for imovel in imoveis:
            ultima_movimentacao = movimentacoes.get(imovel=imovel)
            if ultima_movimentacao:
                lista.append([
                    imovel,
                    Foto.objects.filter(imovel=imovel).get(),
                    ultima_movimentacao,
                ])

        return lista

def temPermissao(request):
    user = request.user
    grupo = user.groups.values_list('name', flat=True)
    if user:
        return True


def aprovarImovel(request, pk=None, historico_pk=None, destaque=False):
    if temPermissao(request):
        imovel = Imovel.objects.get(usuario=request.user, pk=pk)
        historico_atual = Historico.objects.get(pk=historico_pk)
        
        if imovel and historico_atual and historico_atual.pendente:
            if destaque and imovel.publicado:
                imovel.destacado = True
            else:
                imovel.publicado = True

            imovel.save()

            historico_atual.pendente = False
            historico_atual.save()

            historico = Historico.objects.create(imovel=imovel, movimentado_por=request.user)
            historico.pendente = False
            historico.motivo = f"{historico_atual.motivo} (Aprovado)"
            historico.save()
            
            return redirect("adm")


def rejeitarImovel(request, historico_pk=None):
    if temPermissao(request):
        historico_atual = Historico.objects.get(pk=historico_pk)
        if historico_atual and historico_atual.pendente:
            historico_atual.pendente = False
            historico_atual.save()

            historico = Historico.objects.create(imovel=historico_atual.imovel, movimentado_por=request.user)
            historico.pendente = False
            historico.motivo = f"{historico_atual.motivo} (Rejeitado)"
            historico.save()
            return redirect("adm")
        
            
            