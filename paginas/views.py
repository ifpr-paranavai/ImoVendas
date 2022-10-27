from cadastros.models import Foto, Imovel
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


class Index(ListView):
    model = Imovel
    template_name = 'paginas/index.html'

    def get_queryset(self):
        lista = [[], [], []]

        proximos = Imovel.objects.filter(publicado=True)[:6]
        destaques = Imovel.objects.filter(destacado=True, publicado=True)[:6]
        novos = Imovel.objects.filter(publicado=True).order_by('cadastrado_em')[:6]

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
        imovel = get_object_or_404(Imovel, pk=self.kwargs['pk'])
        fotos = Foto.objects.filter(imovel=imovel)
        imovel_count = Imovel.objects.filter(usuario=imovel.usuario).count()
        return [imovel, fotos, imovel_count]


class ImovelBoost(DetailView):
    model = Imovel
    template_name = 'paginas/imovel-boost.html'

    def get_object(self):
        imovel = get_object_or_404(Imovel, pk=self.kwargs['pk'], usuario=self.request.user)
        fotos = Foto.objects.filter(imovel=imovel)
        return [imovel, fotos]
        
    