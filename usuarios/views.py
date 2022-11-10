from cadastros.models import Perfil
from django.contrib.auth.models import User, Group
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView

from usuarios.forms import UsuarioForm, PerfilUpdateForm



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

            grupo_usuario = Group.objects.get_or_create(name="Usuario")

            self.object.groups.add(grupo_usuario[0])
            self.object.save()


        except:
            perfil.delete()
            self.object.delete()
            form.add_error(None, 'Ocorreu um erro ao cadastrar o usuário')
            return self.form_invalid(form)

        return url

class PerfilUpdate(UpdateView):
    form_class = PerfilUpdateForm
    template_name = "usuarios/form-update.html"
    success_url = reverse_lazy("index")
    model = Perfil


    def get_object(self):
        perfil = Perfil.objects.get(usuario__pk=self.kwargs["pk"])
        
        if perfil.usuario != self.request.user:
            raise PermissionError("Você não possui permissão para acessar essa página.")

        return perfil