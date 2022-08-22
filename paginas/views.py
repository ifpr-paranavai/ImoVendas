from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from cadastros.models import Imovel



class Index(ListView):
    model = Imovel
    template_name = 'paginas/index.html'


class ImovelView(DetailView):
    model = Imovel
    template_name = 'paginas/ver_imovel.html'