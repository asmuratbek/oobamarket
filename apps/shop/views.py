from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import FormView
from django.views.generic import UpdateView
from slugify import slugify

from apps.product.forms import ProductForm
from apps.product.models import Product
from apps.shop.forms import ShopForm, ShopBannersForm, ShopSocialLinksForm
from apps.users.mixins import AddProductMixin, AddBannerMixin, AddSocialLinksMixin
from .models import Shop, SocialLinks


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
        form.instance.slug = slugify(form.instance.title)
        form.save(commit=False)
        form.save()
        form.instance.user.add(self.request.user)
        return super(ShopCreateView, self).form_valid(form)


class ShopUpdateView(LoginRequiredMixin, UpdateView):
    model = Shop
    form_class = ShopForm
    template_name = 'shop/shop_update.html'


class ShopBannersView(LoginRequiredMixin, AddBannerMixin, CreateView):
    form_class = ShopBannersForm
    template_name = 'shop/shop_banner.html'

    def get_success_url(self):
        return reverse('shops:detail', kwargs={'slug': self.kwargs['slug']})

    def get_initial(self):
        return {'user': self.request.user,
                'shop': Shop.objects.get(slug=self.kwargs['slug'])}

    def form_valid(self, form, **kwargs):
        form.instance.shop = Shop.objects.get(slug=self.kwargs['slug'])
        form.save()
        return super(ShopBannersView, self).form_valid(form)


class ShopBannerDeleteView(LoginRequiredMixin, AddBannerMixin, DeleteView):
    pass


# class ShopSocialLinksView(LoginRequiredMixin, AddSocialLinksMixin, CreateView):
#     form_class = ShopSocialLinksForm
#     template_name = 'shop/shop_social_update.html'
#
#     def get_success_url(self):
#         return reverse('shops:detail', kwargs={'slug': self.kwargs['slug']})
#
#     def get_initial(self):
#         return {'user': self.request.user,
#                 'shop': Shop.objects.get(slug=self.kwargs['slug'])}
#
#     def form_valid(self, form, **kwargs):
#         form.instance.shop = Shop.objects.get(slug=self.kwargs['slug'])
#         form.save()
#         return super(ShopSocialLinksView, self).form_valid(form)

class ShopSocialLinksUpdateView(LoginRequiredMixin, AddSocialLinksMixin, UpdateView):
    model = SocialLinks
    form_class = ShopSocialLinksForm
    template_name = 'shop/shop_social_update.html'

    def get_object(self, queryset=None):
        try:
            social = SocialLinks.objects.get(shop__slug=self.kwargs['slug'])
        except SocialLinks.DoesNotExist:
            social = SocialLinks.objects.create(shop=Shop.objects.get(slug=self.kwargs['slug']))
        return social

    def get_success_url(self):
        return reverse('shops:detail', kwargs={'slug': self.kwargs['slug']})

    def get_initial(self):
        return {'user': self.request.user,
                'shop': Shop.objects.get(slug=self.kwargs['slug'])}

    def form_valid(self, form, **kwargs):
        form.instance.shop = Shop.objects.get(slug=self.kwargs['slug'])
        form.save()
        return super(ShopSocialLinksUpdateView, self).form_valid(form)

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
