from cadastros.models import Cidade, Imovel
from dal import autocomplete
from django import forms


class ImovelForm(forms.ModelForm):
    cidade = forms.ModelChoiceField(
        queryset=Cidade.objects.all().order_by("nome").select_related("estado"),
        widget=autocomplete.ModelSelect2(
            url="cidade-autocomplete",
            attrs={
                "data-placeholder": "Buscar cidade...",
                "data-minimum-input-length": 3,
            },
        ),
    )

    class Meta:
        model = Imovel
        fields = ["titulo", "descricao", "preco", "cep", "rua", "bairro", "numero",
              "cidade", "quantidade_quartos", "quantidade_banheiros", "area", "tipo", "finalidade"]
        