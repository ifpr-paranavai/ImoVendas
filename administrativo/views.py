from django.views.generic import TemplateView
from braces.views import GroupRequiredMixin

class Adm(GroupRequiredMixin, TemplateView):
    group_required = u'Administrador'
    template_name = "administrativo/index.html"
