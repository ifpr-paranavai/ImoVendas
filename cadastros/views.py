from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Imovel

# Create your views here.


class ImovelCreate(CreateView):
    model = Imovel
    fields = ["titulo", "descricao", "preco", "cep", "rua", "bairro", "numero",
              "cidade", "quantidade_quartos", "quantidade_banheiros", "area", "tipo", "finalidade", "usuario",]
    template_name = "cadastros/imovel-form.html"
    success_url = reverse_lazy('index')
