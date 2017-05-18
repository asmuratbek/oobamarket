from django import template
from django.http import request
from django.utils.html import mark_safe
from django.urls import reverse

register = template.Library()

@register.assignment_tag
def show_add_product_button(shop, user):
    if user.is_authenticated:
        if shop.is_owner(user):
            return mark_safe('''
                            <li class="active">
                            <a href="%s">
                            Добавить Товары</a></li>
                                ''' % reverse('product:add_product', kwargs={'slug':shop.slug}))
        else:
            return mark_safe('')
