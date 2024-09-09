from django import template

register = template.Library()


@register.filter
def is_user(user):
    return user.is_authenticated and user.groups.filter(name="Profile").exists()
