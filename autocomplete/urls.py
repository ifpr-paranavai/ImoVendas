from django.urls import path
from .views import CidadeAutocomplete

urlpatterns = [
    path('buscar-cidade/', CidadeAutocomplete.as_view(), name='cidade-autocomplete'),
]


