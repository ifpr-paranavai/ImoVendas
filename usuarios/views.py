from tabnanny import verbose
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.forms import CharField, PasswordInput, ModelForm

from cadastros.models import Perfil

# Create your views here.

class PerfilForm(ModelForm):
    nome_de_usuario = CharField(help_text="Digite o seu nome de usuário", max_length=80)
    senha = CharField(widget=PasswordInput, help_text="Digite sua senha")
    senha_repetida = CharField(widget=PasswordInput, help_text="Repita a senha digitada")

    class Meta:
        model = Perfil
        exclude = ["usuario"]
        


class PerfilCreate(CreateView):
    form_class = PerfilForm
    template_name = "usuarios/cadastro-form.html"
    success_url = reverse_lazy('index')
    model = Perfil


    def form_valid(self, form):

        if form.cleaned_data["senha"] == form.cleaned_data["senha_repetida"]:
            usuario = User.objects.create_user(form.cleaned_data["nome_de_usuario"], form.instance.email, form.cleaned_data["senha"])
        

        form.instance.usuario = usuario

        url = super().form_valid(form)

        return url
