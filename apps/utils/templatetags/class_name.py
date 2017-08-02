from django import template

register = template.Library()


@register.filter(name='class_name')
def obj_class_name(obj):
    return obj.__class__.__name__
