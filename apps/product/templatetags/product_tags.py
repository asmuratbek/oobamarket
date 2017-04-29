from django import template
from ..models import Product
from apps.users.models import User


register = template.Library()

@register.assignment_tag
def is_favorite(product, user):
    if product.favorite.filter(user=user).exists():
        return 'Удалить из избранного'
    else:
        return 'Добавить в избранное'


@register.assignment_tag
def is_in_cart(product, user):
    if product.cartitem_set.filter(cart__user=user).exists():
        return 'Удалить из корзины'
    else:
        return 'Добавить в корзину'

@register.assignment_tag
def is_in_cart_block(product, user):
    if product.cartitem_set.filter(cart__user=user).exists():
        return '''
            <a href="#" class="add-basket">
                        <span class="glyphicon glyphicon-shopping-cart"></span>
                        Добавить в корзину
                    </a>
        '''
    else:
        return '''<a href="#" class="add-basket">
                        <span class="glyphicon glyphicon-shopping-cart"></span>
                        Добавить в корзину
                    </a>'''
