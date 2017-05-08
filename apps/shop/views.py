from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.views.generic import CreateView
from django.views.generic import FormView
from slugify import slugify

from apps.product.forms import ProductForm
from apps.product.models import Product
from apps.shop.forms import ShopForm
from .models import Shop
# Create your views here.


class ShopDetailView(generic.DetailView):
    model = Shop



class ShopCreateView(LoginRequiredMixin,CreateView):
    form_class = ShopForm
    template_name = 'shop/shop_form.html'
    # fields = ['title', 'logo', 'email', 'phone', 'short_description', 'description', 'user', 'slug',]
    def get_success_url(self):
        return reverse('shops:detail', args=(self.object.slug,))

    def form_valid(self, form):
        form.save()
        form.instance.user.add(self.request.user)
        return super(ShopCreateView, self).form_valid(form)

# def shop_add(request):
#     form = ShopForm(request.POST, files=request.FILES)
#     if request.method == 'POST':
#         if form.is_valid():
#             print(form.cleaned_data)
#             shop = form.save(commit=False)
#             shop.save()
#         else:
#             print(form.errors)
#
#     params = {
#         'form': form,
#     }
#     return render(request, 'shop/shop_form.html', params)


class ProductCreateView(LoginRequiredMixin, CreateView):
    form_class = ProductForm
    template_name = 'shop/product_form.html'

    def get_success_url(self):
        return reverse('shops:detail', args=(self.object.slug,))


    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        form.save(commit=False)
        return super(ProductCreateView, self).form_valid(form)

    # def post(self, form):
    #     form.instance.shop = self.request.shop.slug
    #     return super(ProductCreateView, self).get_default_shop(form)

    # def get_context_data(self, **kwargs):
    #     data = {}
    #     data['shop_id'] =
    #     # call the super to get the default context
    #     context = super(ProductCreateView, self).get_context_data(**kwargs)
    #
    #     # add the initial value here
    #     # but first get the id from the request GET data
    #     id = self.request.GET.get('shop_id')
    #     # again: do some checking of id
    #     context.get('form').initial['shop'] = id
    #
    #     return context


# class ProductFormView(LoginRequiredMixin, FormView):
#     form_class = ProductForm
#     template_name = 'shop/product_form.html'
#
#
#     def get_success_url(self):
#         return reverse('shop:detail', args=(self.object.slug,))
#
#     def post(self, form):
#         form.instance.shop = self.request.shop.slug
#         return super(ProductCreateView, self).get_default_shop(form)


def create(request):

    params = {
        'shop': 'shop'
    }

    return render(request, 'shop/create.html', params)

def agreement(request):

    params = {
        'shop': 'shop'
    }

    return render(request, 'shop/agreement.html', params)
