
from django import template

register = template.Library()

@register.filter(name='get_group')
def get_group(user):
    group_name = ""
    for group in user.groups.all():
        group_name += f"{group.name} "
    return group_name
