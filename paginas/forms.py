from cadastros.models import Movimentacao
from django import forms

class MovimentacaoForm(forms.ModelForm):
    comprovante = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}), help_text="Insira o comprovante")

    class Meta:
        model = Movimentacao
        fields = ["comprovante"]




    