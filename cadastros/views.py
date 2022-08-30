from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from cadastros.forms import ImovelFotoForm
from datetime import date, timedelta

# Create your views here.


class ImovelCreate(LoginRequiredMixin, CreateView):
    form_class = ImovelFotoForm
    template_name = "cadastros/imovel-form.html"
    success_url = reverse_lazy('index')

    def form_valid(self, form):

        form.instance.usuario = self.request.user
        form.instance.expira_em = date.today() + timedelta(days=30)

        url = super().form_valid(form)

        return url
