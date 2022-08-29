from cadastros.models import Perfil
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from usuarios.forms import UsuarioForm



class PerfilCreate(CreateView):
    form_class = UsuarioForm
    template_name = "usuarios/cadastro-form.html"
    success_url = reverse_lazy("index")
    model = User


    def form_valid(self, form):

        url = super().form_valid(form)

        try:
            perfil = Perfil.objects.create(
                usuario=self.object,
                nome=form.cleaned_data["nome"],
                cpf=form.cleaned_data["cpf"],
                celular=form.cleaned_data["celular"],
                cidade=form.cleaned_data["cidade"],
            )
        except:
            self.object.delete()
            form.add_error(None, 'Ocorreu um erro ao cadastrar o usuário')
            return self.form_invalid(form)

        return url
