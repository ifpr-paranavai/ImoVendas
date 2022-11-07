
from django import template

register = template.Library()

@register.filter(name='is_admin')
def is_admin(user):
    if user:
        return user.groups.filter(name="Administrador").exists()

    return False
