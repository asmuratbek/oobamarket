from .models import Cart


def cart_count(request):
    if request.session.get("cart_id"):
        cart_id = request.session.get("cart_id")
        cart, created = Cart.objects.get_or_create(id=cart_id)
        item_count = cart.cartitem_set.count()
    elif request.user.is_authenticated() and request.user.cart_set.exists():
        item_count = request.user.get_cart_count()
    else:
        item_count = 0
    return {
        'cart_count': item_count
    }
