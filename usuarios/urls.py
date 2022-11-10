from django.urls import path
from django.contrib.auth import views as auth_views
from .views import PerfilCreate, PerfilUpdate

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/form-login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cadastro/', PerfilCreate.as_view(template_name='usuarios/form-cadastro.html'), name='cadastro'),
    path('editar/perfil/<int:pk>', PerfilUpdate.as_view(template_name='usuarios/form-update.html'), name='editar-perfil'),
]
