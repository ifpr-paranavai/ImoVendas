from cadastros.models import Cidade
from dal import autocomplete
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UsuarioForm(UserCreationForm):
    nome = forms.CharField(max_length=100)
    celular = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'data-mask':"(00) 00000-0000"}))
    email = forms.EmailField(max_length=100)
    cpf = forms.CharField(max_length=15, label="CPF", widget=forms.TextInput(attrs={'data-mask':"000.000.000-00"}))
    
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

    username = forms.CharField(max_length=20, label="Nome de Usuário")

    class Meta:
        model = User
        fields = [
            "nome",
            "celular",
            "cidade",
            "email",
            "cpf",
            "username",
            "password1",
            "password2",
        ]
        
        

    def clean_email(self):
        e = self.cleaned_data["email"]
        if User.objects.filter(email=e).exists():
            raise ValidationError(f"O email ${e} já está em uso.")

        return e

class PerfilUpdateForm(forms.ModelForm):
    nome = forms.CharField(max_length=100)
    celular = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'data-mask':"(00) 00000-0000"}))
    
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
        model = User
        fields = [
            "nome",
            "celular",
            "cidade",
        ]
        
    def clean_email(self):
        e = self.cleaned_data["email"]
        if User.objects.filter(email=e).exists():
            raise ValidationError(f"O email ${e} já está em uso.")

        return e

        
