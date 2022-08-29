from cadastros.models import Cidade, Imovel
from dal import autocomplete
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Fieldset, ButtonHolder, Div, HTML

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.layout = Layout(
            Fieldset(
                'Detalhes do anúncio',
                Row(
                    Column('titulo', css_class='form-group col-lg mb-0'),
                    Column('preco', css_class='form-group col-lg-4 mb-0'),
                ),
                Column('descricao', css_class='form-group col-sm mb-0'),
                Column('finalidade', css_class='form-group col-sm mb-0'),
                css_class="mb-5"
            ),
            Fieldset(
                'Endereço',
                Row(
                    Column('cep', css_class='form-group col-lg mb-0'),
                    Column('numero', css_class='form-group col-lg mb-0'),
                    Column('bairro', css_class='form-group col-lg-4 mb-0'),
                ),
                Row(
                    Column('rua', css_class='form-group col-lg mb-0'),
                    Column('cidade', css_class='form-group col-lg mb-0'),
                ),
                css_class="mb-5"
            ),
            Fieldset(
                'Características do imóvel',
                Row(
                    Column('tipo', css_class='form-group col-sm mb-0'),
                    
                ),
                Row(
                    Column('quantidade_quartos', css_class='form-group col-lg mb-0'),
                    Column('quantidade_banheiros', css_class='form-group col-lg mb-0'),
                    Column('area', css_class='form-group col-sm mb-0'),
                ),
                css_class="mb-5"
            ),
            
            ButtonHolder(
                    Div(
                        HTML("""
                            <button type="submit" class="btn btn-lg btn-success w-100 fs-4">
                                Salvar
                            </button>
                        """),
                        css_class="w-50 mx-auto"
                    ),
                )
            )  
            
        