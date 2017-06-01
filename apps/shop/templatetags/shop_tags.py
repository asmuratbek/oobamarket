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
                            <div class="col-md-4 col-sm-6">
                            <div class="cover">
                                <a class="url-item" href="%s"></a>
                                <div class="add-product">
                                    <i class="glyphicon glyphicon-plus-sign"></i>
                                    <p>Добавить новый товар</p>
                                </div>

                                <div class="stock">
                                    <a href="#">Добавить акцию</a>
                                </div>
                            </div>
                        </div>
                                ''' % reverse('product:add_product', kwargs={'slug':shop.slug}))
        else:
            return mark_safe('')

@register.assignment_tag
def show_add_banner_button(shop, user):
    if user.is_authenticated:
        if shop.is_owner(user):
            return mark_safe('''
                            <div class="auch-edit">
                                <a href="%s" >
                                    <i class="glyphicon glyphicon-cog" data-toggle="tooltip" title="" data-placement="top" data-original-title="Редактировать баннер"></i>
                                </a>
                            </div>
                                ''' % reverse('shops:add_banner', kwargs={'slug': shop.slug}))
        else:
            return mark_safe('')


@register.assignment_tag
def show_add_social_button(shop, user):
    if user.is_authenticated:
        if shop.is_owner(user):
            return mark_safe('''
                            <div class="auch-edit">
                                <a href="%s">
                                    <i class="glyphicon glyphicon-cog" data-toggle="tooltip" title="" data-placement="right" data-original-title="Редактировать соц.сети"></i>
                                </a>
                            </div>
                                ''' % reverse('shops:update_social', kwargs={'slug': shop.slug }))
        else:
            return mark_safe('')




