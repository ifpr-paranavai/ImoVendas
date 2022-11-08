from datetime import datetime, timedelta
import uuid

from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from geocoder import ip

from cadastros.models import Foto, Movimentacao, Imovel
from paginas.forms import MovimentacaoForm


class Index(ListView):
    model = Imovel
    template_name = 'paginas/index.html'

    def get_queryset(self):
        lista = [[], [], []]
        
        proximos = Imovel.objects.filter(negociado=False, publicado=True, cidade__nome=ip("me").city)[:6]
        destaques = Imovel.objects.filter(destacado=True, publicado=True, negociado=False)[:6]
        novos = Imovel.objects.filter(publicado=True, negociado=False).order_by('cadastrado_em')[:6]

        for imovel in proximos:
            lista[0].append([imovel, Foto.objects.filter(imovel=imovel)])

        for imovel in destaques:
            lista[1].append([imovel, Foto.objects.filter(imovel=imovel)])
            
        for imovel in novos:
            lista[2].append([imovel, Foto.objects.filter(imovel=imovel)])

        return lista


class ImovelView(DetailView):
    model = Imovel
    template_name = 'paginas/imovel-view.html'

    def get_object(self):
        if self.request.user.groups.filter(name="Administrador").exists():
            imovel = get_object_or_404(Imovel, pk=self.kwargs['pk'])
        else:
            imovel = get_object_or_404(Imovel, pk=self.kwargs['pk'], publicado=True, negociado=False)

        fotos = Foto.objects.filter(imovel=imovel)
        imovel_count = Imovel.objects.filter(usuario=imovel.usuario).count()
        return [imovel, fotos, imovel_count]


class ImovelBoost(CreateView):
    template_name = 'paginas/imovel-boost.html'
    form_class = MovimentacaoForm
    success_url = reverse_lazy('listar-imovel')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["imovel"] = get_object_or_404(Imovel, pk=self.kwargs["pk"], usuario=self.request.user)
        context["ultima_mov"] = Movimentacao.objects.latest("movimentado_em")
        context["fotos"] = Foto.objects.filter(imovel=context["imovel"])

        return context


    def form_valid(self, form):
        form.instance.motivo = "Destaque de imóvel"
        form.instance.movimentado_por = self.request.user
        form.instance.imovel = get_object_or_404(Imovel, pk=self.kwargs["pk"], usuario=self.request.user)
        
        comprovante = self.request.FILES.getlist("comprovante")[0]
        ext = comprovante.name.split(".")[-1]
        comprovante.name = f"{uuid.uuid4()}.{ext}" 
        form.instance.comprovante = comprovante

        return super().form_valid(form)

     

class ImovelRenew(DetailView):
    model = Imovel
    template_name = 'paginas/imovel-renew.html'

    def get_object(self):
        imovel = get_object_or_404(Imovel, pk=self.kwargs['pk'], usuario=self.request.user)
        fotos = Foto.objects.filter(imovel=imovel)

        imovel.publicado = True
        imovel.expira_em = datetime.now() + timedelta(30)
        imovel.save()
        
        historico = Movimentacao.objects.create(imovel=imovel, movimentado_por=self.request.user)
        historico.motivo = "Renovação de imóvel"
        historico.save()

        return [imovel, fotos]
        
        
        
    