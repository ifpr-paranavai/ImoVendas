from crispy_forms.helper import FormHelper
from crispy_forms.layout import (HTML, ButtonHolder, Column, Div, Fieldset,
                                 Layout, Row)
from dal import autocomplete
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import (BooleanField, CharField, DecimalField, Form, IntegerField,
                          ModelChoiceField)

from cadastros.models import Cidade, Imovel, Tipo


class ImovelSearchForm(Form):
    cidade = forms.ModelChoiceField(
        required=False,
        queryset=Cidade.objects.all().order_by("nome").select_related("estado"),
        widget=autocomplete.ModelSelect2(
            url="cidade-autocomplete",
            attrs={
                "data-placeholder": "Buscar cidade...",
                "data-minimum-input-length": 3,
            },
        ),
    )
    quartos = IntegerField(required=False, validators=[MinValueValidator(0), MaxValueValidator(99)], help_text="Quantidade de quartos")
    banheiros = IntegerField(required=False, validators=[MinValueValidator(0), MaxValueValidator(99)], help_text="Quantidade de banheiros")
    bairro = CharField(required=False, help_text="Bairro do imóvel")
    categoria = ModelChoiceField(
        queryset=Tipo.objects.all(),
        required=False,
        empty_label="-"
    )
    preco_max = DecimalField(required=False, help_text="Preço máximo do imóvel", label="Preço")
    destacado = BooleanField(required=False, label="Somente Destacado", help_text="Mostrar somente imóveis destacados")
    local = BooleanField(required=False, label="Somente Local", help_text="Mostrar somente imóveis da sua cidade")
    
    

    class Meta:
        fields = [
            "cidade",
            "quartos",
            "banheiros",
            "bairro",
            "preco_max",
            "categoria",
            "destacado",
            "local",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.layout = Layout(
            
            Row(
                Column("cidade", css_class="form-group co-lg-2 mb-0"),
                Column("bairro", css_class="form-group co-lg-6 mb-0"),
                Column("quartos", css_class="form-group col-lg-2 mb-0"),
                Column("banheiros", css_class="form-group col-lg-2 mb-0"),
            ),
            Row(
                Column("categoria", css_class="form-group co-lg-4 mb-0"),
                Column("preco_max", css_class="form-group co-lg-4 mb-0"),
            ),
            Row(
                Column("destacado", css_class="form-group col-lg-6 mb-0"),
                Column("local", css_class="form-group col-lg-6 mb-0"),
            ),
            ButtonHolder(
                Div(
                    HTML(
                        """
                        <button type="submit" class="btn bgMainColor hoverTransition text-white w-100 fs-5 my-4">
                            Aplicar
                        </button>
                    """
                    ),
                    css_class="w-25 mx-auto",
                ),
            ),
        )


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
        fields = [
            "titulo",
            "descricao",
            "preco",
            "cep",
            "rua",
            "bairro",
            "numero",
            "cidade",
            "quantidade_quartos",
            "quantidade_banheiros",
            "area",
            "tipo",
            "finalidade",
        ]

        widgets = {
            "cep": forms.TextInput(attrs={"data-mask": "00000-000"}),
        }


class ImovelFotoForm(ImovelForm):
    fotos = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        help_text="Insira as multiplas fotos do imóvel",
    )

    class Meta(ImovelForm.Meta):
        fields = ImovelForm.Meta.fields + ["fotos"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.layout = Layout(
            Fieldset(
                "Detalhes do anúncio",
                Row(
                    Column("titulo", css_class="form-group col-lg mb-0"),
                    Column("preco", css_class="form-group col-lg-4 mb-0"),
                ),
                Column("descricao", css_class="form-group col-sm mb-0"),
                Column("finalidade", css_class="form-group col-sm mb-0"),
                css_class="mb-5",
            ),
            Fieldset(
                "Endereço",
                Row(
                    Column("cep", css_class="form-group col-lg mb-0"),
                    Column("numero", css_class="form-group col-lg mb-0"),
                    Column("bairro", css_class="form-group col-lg-4 mb-0"),
                ),
                Row(
                    Column("rua", css_class="form-group col-lg mb-0"),
                    Column("cidade", css_class="form-group col-lg mb-0"),
                ),
                css_class="mb-5",
            ),
            Fieldset(
                "Características do imóvel",
                Row(
                    Column("tipo", css_class="form-group col-sm mb-0"),
                ),
                Row(
                    Column("quantidade_quartos", css_class="form-group col-lg mb-0"),
                    Column("quantidade_banheiros", css_class="form-group col-lg mb-0"),
                    Column("area", css_class="form-group col-sm mb-0"),
                ),
                css_class="mb-5",
            ),
            Fieldset(
                "Fotos do imóvel",
                HTML(
                    """
                    <a id="showModal" href="javascript:void(0)" class="btn text-white bgMainColor hoverTransition p-2">
                        <i class="fa-solid fa-circle-question fa-2xl"></i>
                        Ajuda
                    </a>
                    <div id="idPreview" class="my-5 col"></div>
                    """
                ),
                Column("fotos", css_class="form-group col-sm mb-0"),
                css_class="mb-5",
            ),
            ButtonHolder(
                Div(
                    HTML(
                        """
                        <button type="submit" class="btn btn-lg bgMainColor hoverTransition text-white w-100 fs-4">
                            Salvar
                        </button>
                    """
                    ),
                    css_class="w-50 mx-auto",
                ),
            ),
        )
