from django import template
from django.http import request
from django.utils.html import mark_safe
from django.urls import reverse

register = template.Library()


@register.assignment_tag
def show_add_product_button(shop, user):
    if not user.is_anonymous:
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
                                    ''' % reverse('product:add_product', kwargs={'slug': shop.slug}))
            elif not shop.is_owner(user):
                return mark_safe('')
    else:
        return mark_safe('')


@register.assignment_tag
def show_add_banner_button(shop, user):
    if not user.is_anonymous:
        if user.is_authenticated:
            if shop.is_owner(user):
                return mark_safe('''
                                <div class="auch-edit" data-toggle="tooltip" title="" data-placement="left" data-original-title="Редактировать баннер">
                                    <a href="%s" >
                                        <i class="glyphicon glyphicon-cog" ></i>
                                    </a>
                                </div>
                                    ''' % reverse('shops:add_banner', kwargs={'slug': shop.slug}))
            elif not shop.is_owner(user):
                return mark_safe('')
    else:
        return mark_safe('')


@register.assignment_tag
def show_add_social_button(shop, user):
    if not user.is_anonymous:
        if user.is_authenticated:
            if shop.is_owner(user):
                return mark_safe('''
                                <div class="auch-edit" data-toggle="tooltip" title="" data-placement="left" data-original-title="Редактировать соц.сети">
                                    <a href="%s" >
                                        <i class="glyphicon glyphicon-cog" ></i>
                                    </a>
                                </div>
                                    ''' % reverse('shops:update_social', kwargs={'slug': shop.slug}))
            elif not shop.is_owner(user):
                return mark_safe('')
    else:
        return mark_safe('')


@register.assignment_tag
def show_edit_shop_button(shop, user):
    if not user.is_anonymous:
        if user.is_authenticated:
            if shop.is_owner(user):
                return mark_safe('''
                                <div class="auch-edit" data-toggle="tooltip" title="" data-placement="left" data-original-title="Редактировать настройки магазина">
                                    <a href="%s" >
                                        <i class="glyphicon glyphicon-cog" ></i>
                                    </a>
                                </div>
                                    ''' % reverse('shops:update', kwargs={'slug': shop.slug}))
            elif not shop.is_owner(user):
                return mark_safe('')
    else:
        return mark_safe('')

@register.assignment_tag
def show_create_sale_button(shop, user):
    if not user.is_anonymous:
        if user.is_authenticated:
            if shop.is_owner(user):
                return mark_safe('''
                                    <li class="active"><a href="%s">Создать Акцию</a></li>
                                ''' % reverse('shops:add_sale', kwargs={'slug': shop.slug}))
            elif not shop.is_owner(user):
                return mark_safe('')
    else:
        return mark_safe('')

@register.assignment_tag
def show_update_sale_button(shop, sale, user):
    if not user.is_anonymous:
        if user.is_authenticated:
            if shop.is_owner(user):
                return mark_safe('''
                                    <a class="btn add" href="%s">Редактировать</a>
                                ''' % reverse('shops:update_sale', kwargs={'slug': shop.slug, 'pk': sale.pk}))
            elif not shop.is_owner(user):
                return mark_safe('')
    else:
        return mark_safe('')
