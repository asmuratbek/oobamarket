from django import template

from apps.cart.models import Cart
from django.utils.html import mark_safe

register = template.Library()


@register.assignment_tag
def is_favorite(product, user):
    if user.is_authenticated:
        if product.favorite.filter(user=user).exists():
            return mark_safe('''<a class="favorite-btn uk-button uk-button-default favorite active " href="">
                        <span class="uk-margin-small-right" uk-icon="icon: heart"></span>
                        Удалить из избранного</a>''')
        else:
            return mark_safe('''<a class="favorite-btn uk-button uk-button-default  favorite" href="">
                        <span class="uk-margin-small-right" uk-icon="icon:  heart"></span>
                        Добавить в избранное</a>''')
    else:
        return mark_safe('''<a class="favorite uk-button uk-button-default  favorite" href="/accounts/login/">
                        <span class="uk-margin-small-right" uk-icon="icon:  heart"></span>
                        Добавить в избранное</a>''')


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
                    <span class="glyphicon glyphicon-shopping-cart add-basket enable" data-toggle="tooltip"
                     title="" data-placement="top" data-product-id="{product}"
                          data-original-title="В корзине"></span>
            """.format(product=product.id)
        else:
            cart_message = """
                <span class="glyphicon glyphicon-shopping-cart add-basket" data-toggle="tooltip"
                     title="" data-placement="top" data-product-id="{product}"
                          data-original-title="Добавить в корзину"></span>
            """.format(product=product.id)
    else:
        cart_message = """
                    <span class="glyphicon glyphicon-shopping-cart add-basket" data-toggle="tooltip"
                     title="" data-placement="top" data-product-id="{product}"
                          data-original-title="Добавить в корзину"></span>
            """.format(product=product.id)

    return mark_safe(cart_message)


@register.assignment_tag
def is_in_cart(request, product):
    if request.session.get("cart_id"):
        cart_id = request.session.get("cart_id")
        cart, created = Cart.objects.get_or_create(id=cart_id)
        if cart.cartitem_set.filter(product=product).exists():
            cart_message = """
                <a class="basket-btn in-the-basket uk-button uk-button-default  basket active " href="">
                    <span class="uk-margin-small-right" uk-icon="icon:  cart"></span>
                    В корзине
                </a>
            """
        else:
            cart_message = """
                 <a class="basket-btn uk-button uk-button-default  basket" href="">
                     <span class="uk-margin-small-right" uk-icon="icon:  cart"></span>
                     Добавить в корзину
                 </a>
            """
    else:
        cart_message = """
                         <a class="basket-btn uk-button uk-button-default  basket" href="">
                            <span class="uk-margin-small-right" uk-icon="icon:  cart"></span>
                            Добавить в корзину
                        </a>
                    """

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
            return ''

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


