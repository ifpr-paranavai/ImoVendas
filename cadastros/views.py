from datetime import date, timedelta
import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from cadastros.forms import ImovelFotoForm
from cadastros.models import Foto, Movimentacao, Imovel


class ImovelCreate(LoginRequiredMixin, CreateView):
    form_class = ImovelFotoForm
    template_name = "cadastros/imovel-form.html"
    success_url = reverse_lazy('index')

    def form_valid(self, form):

        form.instance.usuario = self.request.user
        form.instance.expira_em = date.today() + timedelta(days=30)
        url = super().form_valid(form)
        
        arquivos = self.request.FILES.getlist("fotos")
        for foto in arquivos:
            ext = foto.name.split(".")[-1]
            foto.name = f"{uuid.uuid4()}.{ext}" 
            Foto.objects.create(imovel=form.instance, foto=foto)

        historico = Movimentacao.objects.create(imovel=form.instance, movimentado_por=self.request.user)
        historico.motivo = "Publicação de imóvel"
        historico.save()

        return url

class ImovelList(LoginRequiredMixin, ListView):
    model = Imovel
    template_name = "cadastros/imovel-list.html"

    def get_queryset(self):
        lista = []
        imoveis = Imovel.objects.filter(usuario=self.request.user)

        for imovel in imoveis:
            lista.append([imovel, Foto.objects.filter(imovel=imovel)])

        
        return lista


def imovelFinish(request, pk=None):
    user = request.user
    if user.is_authenticated:
        imovel = Imovel.objects.get(usuario=user, pk=pk)
        
        if imovel:
            imovel.negociado = True
            imovel.publicado = False
            imovel.save()

            historico = Movimentacao.objects.create(imovel=imovel, movimentado_por=user)
            historico.motivo = "Imóvel negociado"
            historico.pendente = False
            historico.save()
            
            return redirect("listar-imovel")
    
        
class ImovelSearch(ListView):
    model = Imovel
    template_name = "cadastros/imovel-search.html"
    
    def get_queryset(self):
        lista = []
        cidade = self.request.GET.get("cidade", None)
        quartos = self.request.GET.get("quartos", None)
        
        imoveis = Imovel.objects.filter(publicado=True, negociado=False)
        
        if cidade:
            imoveis = imoveis.filter(cidade__nome=cidade)
            
        if quartos:
            imoveis = imoveis.filter(quantidade_quartos=quartos)

        for imovel in imoveis:
            lista.append([imovel, Foto.objects.filter(imovel=imovel)])
            
        return lista