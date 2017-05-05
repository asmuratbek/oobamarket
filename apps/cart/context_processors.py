from .models import Cart


def cart_count(request):
    if request.user.is_authenticated:
        item_count = request.user.get_cart_count()
    else:
        cart_id = request.session.get("cart_id")
        cart, created = Cart.objects.get_or_create(id=cart_id)
        item_count = cart.cartitem_set.count()
    return {
        'cart_count': item_count
    }
