from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import FormView
from django.views.generic import UpdateView
from slugify import slugify

from apps.product.forms import ProductForm
from apps.product.models import Product
from apps.shop.decorators import delete_decorator
from apps.shop.forms import ShopForm, ShopBannersForm, ShopSocialLinksForm
from apps.users.mixins import AddProductMixin, AddBannerMixin, AddSocialLinksMixin, UpdateShopMixin, DeleteShopMixin
from .models import Shop, SocialLinks, Banners


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


class ShopUpdateView(LoginRequiredMixin, UpdateShopMixin, UpdateView):
    model = Shop
    form_class = ShopForm
    template_name = 'shop/shop_update.html'

class ShopDeleteView(LoginRequiredMixin, DeleteShopMixin, DeleteView):
    model = Shop
    template_name = 'layout/modal_product_delete_confirm.html'

    def get_success_url(self):
        return reverse("index")


class ShopBannersView(LoginRequiredMixin, AddBannerMixin, CreateView):
    form_class = ShopBannersForm
    template_name = 'shop/shop_banner.html'

    def get_context_data(self, **kwargs):
        context = super(ShopBannersView, self).get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']
        return context

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


def agreement(request):

    params = {
        'shop': 'shop'
    }

    return render(request, 'shop/agreement.html', params)


class CreateBanners(LoginRequiredMixin, AddBannerMixin, View):
    def get(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        shop = get_object_or_404(Shop, slug=slug)
        banners = shop.banners_set.all()
        return render(self.request, 'shop/shop_banner.html', {'banners': banners,
                                                              'slug': slug})

    def post(self, request, *args, **kwargs):
        form = ShopBannersForm(request.POST, request.FILES)
        if form.is_valid():
            shop = Shop.objects.get(slug=self.kwargs['slug'])
            form.instance.shop = shop
            banner = form.save()
            data = {'is_valid': True, 'banner_id': banner.id, 'name': banner.image.name, 'url': banner.image.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


@login_required
@csrf_exempt
@delete_decorator
def delete_banners(request):
    if request.method == 'POST' and request.is_ajax():
        banner_id = request.POST.get('banner_id', '')
        if banner_id:
            try:
                banner = Banners.objects.get(id=banner_id)
            except Banners.DoesNotExist:
                return JsonResponse({'message': 'Shop Does Not Exist'})
            banner.delete()
            return JsonResponse({'message': 'Banner is succefully delete.'})
        return JsonResponse({'message': 'banner field must not be null.'})
    return JsonResponse({'message': 'Request must be post.'})
