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
from apps.shop.forms import ShopForm, ShopBannersForm
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
        form.save(commit=False)
        form.save()
        form.instance.user.add(self.request.user)
        return super(ShopCreateView, self).form_valid(form)


class ShopBannersView(LoginRequiredMixin, CreateView):
    form_class = ShopBannersForm
    template_name = 'shop/shop_banner.html'

    def get_success_url(self):
        return reverse('shops:detail', kwargs={'slug': self.kwargs['slug']})

    def form_valid(self, form, **kwargs):
        form.instance.shop = Shop.objects.get(slug=self.kwargs['slug'])
        form.save()
        return super(ShopBannersView, self).form_valid(form)


class ProductCreateView(LoginRequiredMixin, CreateView):
    form_class = ProductForm
    template_name = 'shop/product_form.html'

    def get_success_url(self):
        return reverse('shops:detail', args=(self.object.shop.slug,))

    def form_valid(self, form, **kwargs):
        form.instance.slug = slugify(form.instance.title)
        form.instance.shop = Shop.objects.get(slug=self.kwargs['slug'])
        form.save()
        return super(ProductCreateView, self).form_valid(form)


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
