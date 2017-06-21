from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView
from django.views.generic import DeleteView

from django.views.generic import UpdateView
from slugify import slugify
from config.settings import base
from apps.shop.decorators import delete_decorator
from apps.shop.forms import ShopForm, ShopBannersForm, ShopSocialLinksForm, ShopContactInline, ShopInlineFormSet
from apps.users.mixins import AddBannerMixin, AddSocialLinksMixin, UpdateShopMixin, DeleteShopMixin
from .models import Shop, SocialLinks, Banners, Contacts
import random


# Create your views here.
class FormsetMixin(object):
    object = None

    def get(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def post(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def get_formset_class(self):
        return self.formset_class

    def get_formset(self, formset_class):
        return formset_class(**self.get_formset_kwargs())

    def get_formset_kwargs(self):
        kwargs = {
            'instance': self.object
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

class ShopDetailView(generic.DetailView):
    model = Shop


class ShopCreateView(LoginRequiredMixin, FormsetMixin, CreateView):
    form_class = ShopForm
    formset_class = ShopInlineFormSet
    model = Shop
    template_name = 'shop/shop_form.html'

    def get_success_url(self):
        return reverse('shops:detail', args=(self.object.slug,))

    def form_valid(self, form, formset):
        random_int = random.randrange(0, 1010)
        form.instance.slug = slugify(form.instance.title) + str(random_int)
        self.object = form.save()
        form.instance.user.add(self.request.user)
        formset.instance = self.object
        formset.save()
        return super(ShopCreateView, self).form_valid(form)


    # # We populate the context with the forms. Here I'm sending
    # # the inline forms in `inlines`
    # def get_context_data(self, **kwargs):
    #     ctx = super(ShopCreateView, self).get_context_data(**kwargs)
    #     if self.request.POST:
    #         ctx['inlines'] = ShopInlineFormSet(self.request.POST)
    #         ctx['inlines'] = ShopInlineFormSet(self.request.POST)
    #     else:
    #         ctx['form'] = ShopForm()
    #         ctx['inlines'] = ShopInlineFormSet()
    #     return ctx


class ShopUpdateView(LoginRequiredMixin, UpdateShopMixin, UpdateView):
    model = Shop
    form_class = ShopForm
    template_name = 'shop/shop_update.html'


class ShopDeleteView(LoginRequiredMixin, DeleteShopMixin, DeleteView):
    model = Shop
    template_name = 'layout/modal_shop_delete_confirm.html'
    success_url = '/'


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
                return JsonResponse({'message': 'Banner does not exist'})
            banner.delete()
            return JsonResponse({'message': 'Banner is succefully delete.'})
        return JsonResponse({'message': 'banner field must not be null.'})
    return JsonResponse({'message': 'Request must be post.'})


@csrf_exempt
def remove_logo(request):
    if request.method == 'POST' and request.is_ajax():
        slug = request.POST.get('slug', '')
        shop = get_object_or_404(Shop, slug=slug)
        if shop.logo:
            shop.logo = base.DEFAULT_IMAGE
            shop.save()
            return JsonResponse({'message': 'Logo removed'})
        return JsonResponse({'message': 'Shop does not have logo'})
