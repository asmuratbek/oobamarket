from django import template

from apps.cart.models import Cart
from ..models import Product
from apps.users.models import User
from django.utils.html import mark_safe


register = template.Library()


@register.assignment_tag
def is_favorite(product, user):
    if user.is_authenticated:
        if product.favorite.filter(user=user).exists():
            return mark_safe('''<a class="favorite-btn active" href="">
                        <span class="glyphicon glyphicon-heart"></span>
                        Удалить из избранного</a>''')
        else:
            return mark_safe('''<a class="favorite-btn" href="">
                        <span class="glyphicon glyphicon-heart"></span>
                        Добавить в избранное</a>''')
    else:
        return mark_safe('''<a class="favorite" href="/accounts/login/">
                        <span class="glyphicon glyphicon-heart"></span>
                        Добавить в избранное</a>''')


@register.assignment_tag
def cart_message(request, product):
    if request.session.get("cart_id"):
        cart_id = request.session.get("cart_id")
        cart, created = Cart.objects.get_or_create(id=cart_id)
        if cart.cartitem_set.filter(product=product).exists():
            cart_message = """
                <input type="submit" value="В корзине" class="add-basket in-the-basket add-to-cart-submit">
            """
        else:
            cart_message = """
                <input type="submit" value="Добавить в корзину" class="add-basket add-to-cart-submit">
            """
    else:
        cart_message = """
                        <input type="submit" value="Добавить в корзину" class="add-basket add-to-cart-submit">
                    """

    return mark_safe(cart_message)


@register.assignment_tag
def is_in_cart(request, product):
    if request.session.get("cart_id"):
        cart_id = request.session.get("cart_id")
        cart, created = Cart.objects.get_or_create(id=cart_id)
        if cart.cartitem_set.filter(product=product).exists():
            cart_message = """
                <a class="basket-btn in-the-basket" href=""><span class="glyphicon glyphicon-shopping-cart"></span>В корзине</a>
            """
        else:
            cart_message = """
                 <a class="basket-btn" href=""><span class="glyphicon glyphicon-shopping-cart"></span>Добавить в корзину</a>
            """
    else:
        cart_message = """
                         <a class="basket-btn" href=""><span class="glyphicon glyphicon-shopping-cart"></span>Добавить в корзину</a>
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
