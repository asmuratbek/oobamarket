from django import template

register = template.Library()


@register.assignment_tag
def set(val=None):
    return val
