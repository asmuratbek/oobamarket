from django.contrib import messages
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from  django.views.generic.list import ListView
# Create your views here.
from apps.cart.models import Cart
from apps.shop.models import Shop
from .forms import AddressForm, UserAddressForm, SimpleOrderForm
from .mixins import CartOrderMixin, LoginRequiredMixin
from .models import UserAddress, UserCheckout, Order, SimpleOrder


class OrderDetail(DetailView):
    model = Order

    def dispatch(self, request, *args, **kwargs):
        try:
            user_check_id = self.request.session.get("user_checkout_id")
            user_checkout = UserCheckout.objects.get(id=user_check_id)
        except UserCheckout.DoesNotExist:
            user_checkout = UserCheckout.objects.get(user=request.user)
        except:
            user_checkout = None

        obj = self.get_object()
        if obj.user == user_checkout and user_checkout is not None:
            return super(OrderDetail, self).dispatch(request, *args, **kwargs)
        else:
            raise Http404


class OrderList(LoginRequiredMixin, ListView):
    queryset = Order.objects.all()

    def get_queryset(self):
        user_check_id = self.request.user.id
        user_checkout = UserCheckout.objects.get(id=user_check_id)
        return super(OrderList, self).get_queryset().filter(user=user_checkout)


class UserAddressCreateView(CreateView):
    form_class = UserAddressForm
    template_name = "forms.html"
    success_url = "/checkout/address/"

    def get_checkout_user(self):
        user_check_id = self.request.session.get("user_checkout_id")
        user_checkout = UserCheckout.objects.get(id=user_check_id)
        return user_checkout

    def form_valid(self, form, *args, **kwargs):
        form.instance.user = self.get_checkout_user()
        return super(UserAddressCreateView, self).form_valid(form, *args, **kwargs)


class AddressSelectFormView(CartOrderMixin, FormView):
    form_class = AddressForm
    template_name = "orders/address_select.html"

    def dispatch(self, *args, **kwargs):
        b_address, s_address = self.get_addresses()
        if b_address.count() == 0:
            messages.success(self.request, "Please add a billing address before continuing")
            return redirect("user_address_create")
        elif s_address.count() == 0:
            messages.success(self.request, "Please add a shipping address before continuing")
            return redirect("user_address_create")
        else:
            return super(AddressSelectFormView, self).dispatch(*args, **kwargs)

    def get_addresses(self, *args, **kwargs):
        user_check_id = self.request.session.get("user_checkout_id")
        user_checkout = UserCheckout.objects.get(id=user_check_id)
        b_address = UserAddress.objects.filter(
            user=user_checkout,
            type='billing',
        )
        s_address = UserAddress.objects.filter(
            user=user_checkout,
            type='shipping',
        )
        return b_address, s_address

    def get_form(self, *args, **kwargs):
        form = super(AddressSelectFormView, self).get_form(*args, **kwargs)
        b_address, s_address = self.get_addresses()

        form.fields["billing_address"].queryset = b_address
        form.fields["shipping_address"].queryset = s_address
        return form

    def form_valid(self, form, *args, **kwargs):
        billing_address = form.cleaned_data["billing_address"]
        shipping_address = form.cleaned_data["shipping_address"]
        order = self.get_order()
        order.billing_address = billing_address
        order.shipping_address = shipping_address
        order.save()
        return super(AddressSelectFormView, self).form_valid(form, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        return "/checkout/"


class SimpleOrderCreateView(View):
    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        order = SimpleOrder()
        order.name = data['name']
        order.last_name = data['last_name']
        order.phone = data['phone']
        order.address = data['address']
        order.user = request.user if request.user.is_authenticated else None
        cart = Cart.objects.get(id=data['cart'])
        cart.completed = True
        cart.save()
        order.cart = cart
        order.save()
        if request.user.is_authenticated():
            cart = Cart.objects.create(user=request.user)
        else:
            cart = Cart.objects.create()
        request.session["cart_id"] = cart.id
        return HttpResponseRedirect(reverse("order:thanks"))


class ThankYouView(TemplateView):
    template_name = 'order/thanks.html'


def shop_simple_order_list_update(request, slug):
    object_list = SimpleOrder.objects.filter(cart__cartitem__product__shop__slug=slug).distinct()
    shop = Shop.objects.get(slug=slug)

    form = SimpleOrderForm()

    context = {
        'shop': shop,
        'object_list': object_list,
        'form': form,
        'object': shop,

    }

    return render(request, 'order/shop_order_list.html', context)


class ShopSimpleOrderDetailView(DetailView):
    model = SimpleOrder
    template_name = 'order/shop_order_detail.html'


class ShopSimpleOrderUpdateView(LoginRequiredMixin, UpdateView):
    model = SimpleOrder
    template_name = 'order/shop_order_detail.html'
    form_class = SimpleOrderForm


def shop_change_status(request):
    if request.method == 'POST':
        form = SimpleOrderForm(request.POST)
        simple_order = SimpleOrder.objects.get(id=request.POST.get('id'))
        simple_order.status = request.POST.get('status')
        simple_order.save()

        return JsonResponse(dict(messages=True))
    return JsonResponse(dict(messages=False))


@csrf_exempt
def shop_delete_simple_order_list(request):
    if request.POST.get('ids[]'):
        for id in request.POST.getlist('ids[]'):
            SimpleOrder.objects.filter(pk=id).update(is_visible=False)
        return JsonResponse(dict(messages=True))
    return JsonResponse(dict(messages=False))


class UserSimpleOrderListView(ListView):
    model = SimpleOrder
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'order/user_order_list.html'

    def get_queryset(self):
        return SimpleOrder.objects.filter(user__username=self.kwargs['username'])


class UserSimpleOrderDetailView(LoginRequiredMixin, DetailView):
    model = SimpleOrder
    template_name = 'order/user_order_detail.html'



# class SimpleOrderShopListUpdateView(UpdateView):
#     model = SimpleOrder
#     form_class = SimpleOrderForm
#
#     def get_initial(self):
#         return {'user': self.request.user, 'slug': Shop.objects.get(slug=self.l)}
#
#     # def get_object(self, queryset=None):
#     #     return SimpleOrder.objects.get(cart__cartitem__product__shop__slug=self.kwargs['slug'])
#
#     def get_context_data(self, **kwargs):
#         context = super(SimpleOrderShopListUpdateView, self).get_context_data(**kwargs)
#         context['object_list'] = SimpleOrder.objects.filter(self.kwargs['pk']).order_by('-created_at')
#         context['shop'] = Shop.objects.get(slug=self.kwargs['slug'])
#         return context
#
#     # def post(self, request, *args, **kwargs):
#     #     data = request.POST.copy()
#     #     order = get_object_or_404(SimpleOrder, id=data['id'])
#     #     order.status = data['status']
#     #     order.save()
#     #     return HttpResponseRedirect(reverse("order:shop_order_list", kwargs={'slug': self.kwargs['slug']}))
#
#     def form_valid(self, form):
#         form.save()
#         return super(SimpleOrderShopListUpdateView, self).form_valid(form)








# class DeleteSimpleOrderShop(LoginRequiredMixin, DeleteView):
#     model = SimpleOrder
#     template_name = 'layout/modal_order_delete_confirm.html'
#
#     def get_success_url(self):
#         print('lala')
#         return reverse("order:shop_order_list", kwargs={'slug': self.object.user.shop_set.first().slug})
