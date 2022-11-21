
from django import template

register = template.Library()

@register.filter(name='get_group')
def get_group(user):
    group_name = ""
    for group in user.groups.all():
        group_name += f"{group.name} "
    return group_name


@register.filter(name="get_code")
def get_code(motive):
    if 'Publicação' in motive:
        return 0

    elif 'Atualização' in motive:
        return 1

    elif 'Destaque' in motive:
        return 2
