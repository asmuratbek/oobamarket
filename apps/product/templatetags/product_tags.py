from django import template
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


@register.assignment_tag
def is_in_cart(product, user):
    if user.is_authenticated:
        if product.cartitem_set.filter(cart__user=user).exists():
            return 'Удалить из корзины'
        else:
            return 'Добавить в корзину'

@register.assignment_tag
def is_in_cart_block(product, user):
    if user.is_authenticated:
        if not product.cartitem_set.filter(cart__user=user).exists():
            return mark_safe('''
                <a href="#" class="add-basket">
                            <span class="glyphicon glyphicon-shopping-cart"></span>
                            Добавить в корзину
                        </a>
            ''')
        else:
            return mark_safe('''<a href="#" class="add-basket in-the-basket">
                            <span class="glyphicon glyphicon-shopping-cart"></span>
                            Удалить из корзины
                        </a>''')
    else:
        return mark_safe('''
                        <a href="#" class="add-basket">
                                    <span class="glyphicon glyphicon-shopping-cart"></span>
                                    Добавить в корзину
                                </a>
                    ''')

@register.assignment_tag
def is_favorite_for_like(product, user):
    if user.is_authenticated:
        if product.favorite.filter(user=user).exists():
            return 'like'
        else:
            return ''
