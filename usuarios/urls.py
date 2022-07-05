from django.urls import path
from django.contrib.auth import views as auth_views
from .views import PerfilCreate, CidadeAutocomplete

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/form-login.html'), name='login'),
    path('cadastro/', PerfilCreate.as_view(template_name='usuarios/form-cadastro.html'), name='cadastro'),

    path('buscar-cidade/', CidadeAutocomplete.as_view(), name='cidade-autocomplete'),
]
