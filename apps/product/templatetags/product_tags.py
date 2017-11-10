from django import template

from apps.cart.models import Cart
from django.utils.html import mark_safe

register = template.Library()


@register.assignment_tag
def is_favorite(product, user):
    if product.favorite.filter(user=user).exists():
        return mark_safe('''<a class="favorite-btn uk-button uk-button-default active " href="" data-item-id="%s">
                    <span class="uk-margin-small-right" uk-icon="icon: heart"></span>
                    Удалить из избранного</a>''' % product.id)
    else:
        return mark_safe('''<a class="favorite-btn uk-button uk-button-default " href="" data-item-id="%s">
                    <span class="uk-margin-small-right" uk-icon="icon:  heart"></span>
                    Добавить в избранное</a>''' % product.id)


@register.assignment_tag
def cart_message(request, product):
    """
    <a href="#" class="add-basket in-the-basket" data-product-id="{product}">
                        <span class="glyphicon glyphicon-shopping-cart"></span>
                        В корзине
                    </a>
    :param request:
    :param product:
    :return:
    """
    if request.session.get("cart_id"):
        cart_id = request.session.get("cart_id")
        cart, created = Cart.objects.get_or_create(id=cart_id)
        if cart.cartitem_set.filter(product=product).exists():
            cart_message = """ 
                  <a href="#" class="basket cart in uk-margin-medium-left" title="В корзине" data-item-id="{product}" uk-tooltip>
                  <span class=" uk-icon" uk-icon="icon: cart; ratio: 2"></span></a>
            """.format(product=product.id)
        else:
            cart_message = """
            <a href="#" class="basket cart uk-margin-medium-left" title="Добавить в корзину" data-item-id="{product}" uk-tooltip>
                  <span class=" uk-icon" uk-icon="icon: cart; ratio: 2"></span></a>
            """.format(product=product.id)
    else:
        cart_message = """
            <a href="#" class="basket cart uk-margin-medium-left" title="Добавить в корзину" data-item-id="{product}" uk-tooltip>
                  <span class=" uk-icon" uk-icon="icon: cart; ratio: 2"></span></a>
                  
            """.format(product=product.id)

    return mark_safe(cart_message)


@register.assignment_tag
def is_in_cart(request, product):
    if request.session.get("cart_id"):
        cart_id = request.session.get("cart_id")
        cart, created = Cart.objects.get_or_create(id=cart_id)
        if cart.cartitem_set.filter(product=product).exists():
            cart_message = """
                <a class="basket-btn in-the-basket uk-button uk-button-default  basket active " href=""
                    data-item-id="%s">
                    <span class="uk-margin-small-right" uk-icon="icon:  cart"></span>
                    В корзине
                </a>
            """ % product.id
        else:
            cart_message = """
                 <a class="basket-btn uk-button uk-button-default  basket" href=""
                     data-item-id="%s">
                     <span class="uk-margin-small-right" uk-icon="icon:  cart"></span>
                     Добавить в корзину
                 </a>
            """ % product.id
    else:
        cart_message = """
                         <a class="basket-btn uk-button uk-button-default  basket" href=""
                            data-item-id="%s">
                            <span class="uk-margin-small-right" uk-icon="icon:  cart"></span>
                            Добавить в корзину
                        </a>
                    """ % product.id

    return mark_safe(cart_message)

# @register.assignment_tag
# def is_in_cart_block(product, user):
#     if user.is_authenticated:
#         if not product.cartitem_set.filter(cart__user=user).exists():
#             return mark_safe('''
#                 <a href="/cart/?item=%s" class="add-basket">
#                             <span class="glyphicon glyphicon-shopping-cart"></span>
#                             Добавить в корзину
#                         </a>
#             ''') % product.id
#         else:
#             return mark_safe('''<a href="/cart/?item=%s" class="add-basket in-the-basket">
#                             <span class="glyphicon glyphicon-shopping-cart"></span>
#                             Удалить из корзины
#                         </a>''') % product.id
#     else:
#         return mark_safe('''
#                         <a href="/cart/?item=%s" class="add-basket">
#                                     <span class="glyphicon glyphicon-shopping-cart"></span>
#                                     Добавить в корзину
#                                 </a>
#                     ''') % product.id

@register.assignment_tag
def is_favorite_for_like(product, user):
    if user.is_authenticated:
        if product.favorite.filter(user=user).exists():
            return 'like'
        else:
            return 'false'

@register.assignment_tag
def is_favorite_for_tooltip(product, user):
    if user.is_authenticated:
        if product.favorite.filter(user=user).exists():
            return "Удалить из избранных"
        else:
            return "Добавить в избранное"


# @register.assignment_tag
# def update_product_link(user, product):
#     if user.is_authenticated:
#         if user in product.shop.user.all():
#             return format_html('''<h2>
#                                 <a href="/products/{}/update_product">
#                                 Редактировать
#                                 </a>
#                             </h2>''').format(product.slug)
#         else:
#             return ''


