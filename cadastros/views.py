import uuid
from datetime import date, timedelta


from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from geocoder import ip

from cadastros.forms import ImovelFotoForm, ImovelSearchForm
from cadastros.models import Cidade, Foto, Imovel, Movimentacao


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

class ImovelUpdate(LoginRequiredMixin, UpdateView):
    form_class = ImovelFotoForm
    template_name = "cadastros/imovel-form.html"
    success_url = reverse_lazy('index')

    def get_queryset(self):
        return Imovel.objects.filter(pk=self.kwargs["pk"], usuario=self.request.user)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.publicado = False
        url = super().form_valid(form)
        
        arquivos = self.request.FILES.getlist("fotos")
        for foto in arquivos:
            ext = foto.name.split(".")[-1]
            foto.name = f"{uuid.uuid4()}.{ext}" 
            Foto.objects.create(imovel=form.instance, foto=foto)

        historico = Movimentacao.objects.create(imovel=form.instance, movimentado_por=self.request.user)
        historico.motivo = "Atualização de imóvel"
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
    template_name = "cadastros/imovel-search.html"
    paginate_by = 6

    search_form = None
    
    def get_queryset(self):
        
        lista = []
        cidade = self.request.GET.get("cidade", None)
        quartos = self.request.GET.get("quartos", None)
        banheiros = self.request.GET.get("banheiros", None)
        bairro = self.request.GET.get("bairro", None)
        preco_max = self.request.GET.get("preco_max", None)
        categoria = self.request.GET.get("categoria", None)
        only_destaque = self.request.GET.get("destacado", None)
        sort_new = self.request.GET.get("novos", None)
        on_location = self.request.GET.get("local", None)
        from_user = self.request.GET.get("usuario", None)
        
        imoveis = Imovel.objects.filter(publicado=True, negociado=False).select_related("cidade", "cidade__estado")

        if on_location:
            user_ip = self.request.META.get('HTTP_X_FORWARDED_FOR', '')
            ip_info = ip(user_ip) 
            cidade = Cidade.objects.get(nome__icontains=ip_info.city, estado__nome__icontains=ip_info.state).pk

        if from_user:
            imoveis = imoveis.filter(usuario__id=from_user)
        
        if cidade:
            imoveis = imoveis.filter(cidade__pk=cidade)

        if bairro:
            imoveis = imoveis.filter(bairro__icontains=bairro)
            
        if quartos:
            imoveis = imoveis.filter(quantidade_quartos=quartos)

        if banheiros:
            imoveis = imoveis.filter(quantidade_banheiros=banheiros)

        if preco_max:
            imoveis = imoveis.filter(preco__lte=float(preco_max))

        if categoria:
            imoveis = imoveis.filter(tipo=categoria)

        if only_destaque:
            imoveis = imoveis.filter(destacado=True)

        if sort_new:
            imoveis = imoveis.order_by("-cadastrado_em")

        for imovel in imoveis:
            lista.append([imovel, Foto.objects.filter(imovel=imovel)[:1]])

        return lista

    def get(self, request, *args, **kwargs):
        self.search_form = ImovelSearchForm(request.GET)
        self.object_list = self.get_queryset()
        return self.render_to_response(self.get_context_data(form=self.search_form))
        