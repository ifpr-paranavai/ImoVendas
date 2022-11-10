import uuid

from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from geocoder import ip

from cadastros.models import Foto, Movimentacao, Imovel, Perfil
from paginas.forms import MovimentacaoForm


class Index(ListView):
    model = Imovel
    template_name = 'paginas/index.html'

    def get_queryset(self):
        lista = [[], [], []]

        imoveis_validos = Imovel.objects.filter(negociado=False, publicado=True).select_related("cidade", "cidade__estado")
        
        proximos = imoveis_validos.filter(cidade__nome=ip("me").city)[:3]
        destaques = imoveis_validos.filter(destacado=True)[:3]
        novos = imoveis_validos.filter(negociado=False).order_by('-cadastrado_em')[:3]

        for imovel in proximos:
            lista[0].append([imovel, Foto.objects.filter(imovel=imovel)[:1]])

        for imovel in destaques:
            lista[1].append([imovel, Foto.objects.filter(imovel=imovel)[:1]])
            
        for imovel in novos:
            lista[2].append([imovel, Foto.objects.filter(imovel=imovel)[:1]])

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
        perfil = Perfil.objects.get(usuario__id=imovel.usuario.id)
        return [imovel, fotos, imovel_count, perfil]


class ImovelPagar(CreateView):
    template_name = 'paginas/imovel-pay.html'
    form_class = MovimentacaoForm
    success_url = reverse_lazy('listar-imovel')
    modo = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["modo"] = self.modo.capitalize()
        context["imovel"] = get_object_or_404(Imovel, pk=self.kwargs["pk"], usuario=self.request.user)
        context["ultima_mov"] = Movimentacao.objects.latest("movimentado_em")
        context["fotos"] = Foto.objects.filter(imovel=context["imovel"])

        return context


    def form_valid(self, form):
        motivo = ""
        if self.modo == "destacar":
            motivo = "Destaque de imóvel"
        elif self.modo == "renovar":
            motivo = "Renovação de imóvel"

        form.instance.motivo = motivo

        form.instance.movimentado_por = self.request.user
        form.instance.imovel = get_object_or_404(Imovel, pk=self.kwargs["pk"], usuario=self.request.user)
        
        comprovante = self.request.FILES.getlist("comprovante")[0]
        ext = comprovante.name.split(".")[-1]
        comprovante.name = f"{uuid.uuid4()}.{ext}" 
        form.instance.comprovante = comprovante

        return super().form_valid(form)
