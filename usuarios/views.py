from cadastros.models import Cidade, Perfil
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from usuarios.forms import UsuarioForm

from dal import autocomplete

# Create your views here.

class CidadeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        cidades = Cidade.objects.all().select_related("estado")

        if self.q:
            cidades = cidades.filter(nome__icontains=self.q).order_by("nome")

        return cidades


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
