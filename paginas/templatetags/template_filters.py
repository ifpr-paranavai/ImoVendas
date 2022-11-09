
from django import template

register = template.Library()

@register.filter(name='is_admin')
def is_admin(user):
    if user:
        return user.groups.filter(name="Administrador").exists()

    return False


@register.filter(name="build_url")
def build_url(url: str, obj):
    return url + f"={obj}"