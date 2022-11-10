

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (HTML, ButtonHolder, Column, Div,
                                 Layout, Row)
from dal import autocomplete
from django import forms
from django.core.validators import MinValueValidator
from django.forms import Form, IntegerField

from cadastros.models import Cidade


class RelatorioForm(Form):
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

    ano = IntegerField(required=False, validators=[MinValueValidator(2000)])

    class Meta:
        fields = ["ano", "cidade"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.layout = Layout(
            Row(
                Column('ano', css_class='form-group col-lg-6 mb-0', default=2022),
                Column('cidade', css_class='form-group co-lg-6 mb-0'),
            ),
            ButtonHolder(
                Div(
                    HTML("""
                        <button type="submit" class="btn bgMainColor hoverTransition text-white w-100 fs-5">
                            Buscar
                        </button>
                    """),
                    css_class="w-50 mx-auto"
                ),
            )
        )
