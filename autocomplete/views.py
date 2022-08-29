from cadastros.models import Cidade
from dal import autocomplete


class CidadeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        cidades = Cidade.objects.all().select_related("estado")

        if self.q:
            cidades = cidades.filter(nome__icontains=self.q).order_by("nome")

        return cidades