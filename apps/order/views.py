from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.detail import DetailView
from  django.views.generic.list import ListView
# Create your views here.
from apps.cart.models import Cart
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


class SimpleOrderListView(ListView):
    model = SimpleOrder
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_queryset(self):
        return SimpleOrder.objects.filter(user__username=self.kwargs['username'])


class SimpleOrderDetailView(DetailView):
    model = SimpleOrder
    template_name = 'order/order_detail.html'


class SimpleOrderShopListView(ListView):
    model = SimpleOrder
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


    def get_queryset(self):
        return SimpleOrder.objects.filter(cart__cartitem__product__shop__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(SimpleOrderShopListView, self).get_context_data(**kwargs)
        context['form'] = SimpleOrderForm()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        order = get_object_or_404(SimpleOrder, id=data['id'])
        order.status = data['status']
        order.save()
        return HttpResponseRedirect(reverse("order:shop_order_list", kwargs={'slug': self.kwargs['slug']}))



class SimpleOrderShopDetailView(DetailView):
    model = SimpleOrder
    template_name = 'order/order_detail.html'
