from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from cadastros.forms import ImovelFotoForm
from cadastros.models import Foto, Imovel
from datetime import date, timedelta


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
            Foto.objects.create(imovel=form.instance, foto=foto)

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