from django.views.generic.list import ListView

from cadastros.models import Imovel



class Index(ListView):
    model = Imovel
    template_name = 'paginas/index.html'