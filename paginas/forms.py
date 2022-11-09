from cadastros.models import Movimentacao
from django import forms
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    ext = value.name.split(".")[-1]
    exts = ['pdf', 'doc', 'docx', 'jpg', 'png', 'xlsx', 'xls']
    msg = "O comprovante precisa ser um documento. Documentos aceitos: "

    for e in exts:
        msg += f"{e} "

    if not ext.lower() in exts:
        raise ValidationError(msg)

class MovimentacaoForm(forms.ModelForm):
    comprovante = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}), help_text="Insira o comprovante", validators=[validate_file_extension])

    

    class Meta:
        model = Movimentacao
        fields = ["comprovante"]




    