from django.urls import path
from .views import Adm


urlpatterns = [
    path('administrativo/', Adm.as_view(), name='adm'),
]