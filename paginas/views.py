from cadastros.models import Imovel
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


class Index(ListView):
    model = Imovel
    template_name = 'paginas/index.html'

    def get_queryset(self):
        proximos = Imovel.objects.all()[:6]
        destaques = Imovel.objects.filter(destacado=True, publicado=True)[:6]
        novos = Imovel.objects.filter(destacado=True).order_by('cadastrado_em')[:6]

        self.object_list = [proximos, destaques, novos]

        return self.object_list


class ImovelView(DetailView):
    model = Imovel
    template_name = 'paginas/ver_imovel.html'

    def get_object(self):
        imovel = get_object_or_404(Imovel, pk=self.kwargs['pk'])
        imovel_count = Imovel.objects.filter(usuario=imovel.usuario).count()
        return [imovel, imovel_count]
        
    