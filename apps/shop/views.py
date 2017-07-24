from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.urls import reverse
from django.views import View
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView
from django.views.generic import DeleteView

from django.views.generic import UpdateView
from slugify import slugify

from apps.reviews.models import ShopReviews
from apps.shop.mixin import FormsetMixin
from apps.users.models import Subscription, SUBSCRIPTION_TYPES
from config.settings import base
from apps.shop.decorators import delete_decorator
from apps.shop.forms import ShopForm, ShopBannersForm, ShopSocialLinksForm, ShopInlineFormSet, SalesCreateForm, \
    ShopUpdateInlineFormSet, ShopUpdateForm
from apps.users.mixins import ShopMixin
from .models import Shop, SocialLinks, Banners, Contacts, Sales
import random


# Create your views here.


class ShopDetailView(generic.DetailView):
    model = Shop

    def get_context_data(self, **kwargs):
        context = super(ShopDetailView, self).get_context_data(**kwargs)
        try:
            context['subscribe'] = Subscription.objects.get(user=self.request.user, subscription=self.object) if \
                self.request.user.is_authenticated else None
        except Subscription.DoesNotExist:
            context['subscribe'] = None
        context['sub_types'] = SUBSCRIPTION_TYPES
        context['admin'] = self.object.user.all()
        return context


class ShopSaleListView(generic.DetailView):
    model = Shop
    template_name = 'shop/sale.html'


class ShopSaleArchiveView(generic.DetailView):
    model = Shop
    template_name = 'shop/sale_archive.html'


def sale_detail(request, slug, pk):
    shop = get_object_or_404(Shop, slug=slug)
    sale = get_object_or_404(Sales, pk=pk)

    context = {
        'shop': shop,
        'sale': sale
    }

    return render(request, 'shop/sale_detail.html', context)


class SalesCreateView(LoginRequiredMixin, ShopMixin, CreateView):
    form_class = SalesCreateForm
    template_name = 'shop/sale_create.html'

    def get_context_data(self, **kwargs):
        context = super(SalesCreateView, self).get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']
        return context

    def get_success_url(self):
        return reverse('shops:sale', kwargs={'slug': self.kwargs['slug']})

    def get_initial(self):
        return {'user': self.request.user,
                'shop': Shop.objects.get(slug=self.kwargs['slug'])}

    def form_valid(self, form, **kwargs):
        form.instance.shop = Shop.objects.get(slug=self.kwargs['slug'])
        form.save()
        return super(SalesCreateView, self).form_valid(form)


class SalesUpdateView(LoginRequiredMixin, ShopMixin, UpdateView):
    model = Sales
    form_class = SalesCreateForm
    template_name = 'shop/sale_create.html'

    def get_success_url(self):
        return reverse('shops:sale', kwargs={'slug': self.kwargs['slug']})


class ShopAboutUsDetailView(generic.DetailView):
    model = Shop
    template_name = 'shop/about-us.html'


class ShopListView(generic.ListView):
    model = Shop


class ShopContactsView(generic.DetailView):
    model = Shop
    template_name = 'shop/contacts.html'


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
        return super(ShopCreateView, self).form_valid(form, formset)


class ShopUpdateView(LoginRequiredMixin, FormsetMixin, ShopMixin, UpdateView):
    model = Shop
    is_update_view = True
    form_class = ShopUpdateForm
    formset_class = ShopUpdateInlineFormSet
    template_name = 'shop/shop_update.html'



class ShopDeleteView(LoginRequiredMixin, ShopMixin, DeleteView):
    model = Shop
    template_name = 'layout/modal_shop_delete_confirm.html'
    success_url = '/'


class ShopBannersView(LoginRequiredMixin, ShopMixin, CreateView):
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


class ShopBannerDeleteView(LoginRequiredMixin, ShopMixin, DeleteView):
    pass


class ShopSocialLinksUpdateView(LoginRequiredMixin, ShopMixin, UpdateView):
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


class CreateBanners(LoginRequiredMixin, ShopMixin, View):
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
                return JsonResponse({'status': 3, 'message': 'Banner does not exist'})
            banner.delete()
            return JsonResponse({'status': 0, 'message': 'Banner is succefully delete.'})
        return JsonResponse({'status': 1, 'message': 'banner field must not be null.'})
    return JsonResponse({'status': 2, 'message': 'Request must be post.'})


@csrf_exempt
def remove_logo(request):
    if request.method == 'POST' and request.is_ajax():
        slug = request.POST.get('slug', '')
        shop = get_object_or_404(Shop, slug=slug)
        if shop.logo:
            shop.logo = base.DEFAULT_IMAGE
            shop.save()
            return JsonResponse({'status': 0, 'message': 'Logo removed'})
        return JsonResponse({'status': 1, 'message': 'Shop does not have logo'})
    return HttpResponseBadRequest


class ShopReviewListView(generic.DetailView):
    model = Shop
    template_name = 'shop/shop_review.html'

    def get_context_data(self, **kwargs):
        context = super(ShopReviewListView, self).get_context_data(**kwargs)
        context['review'] = ShopReviews.objects.all
        return context


@login_required
def add_shop_review(request, slug):
    if request.is_ajax():
        review = ShopReviews()
        review.text = request.POST.get('text')
        review.shop = Shop.objects.get(slug=slug)
        review.user = request.user
        if request.POST.get('rating'):
            review.stars = '*' * int(request.POST.get('rating'))

        exists_review = ShopReviews.objects.filter(user=review.user, shop=review.shop)

        if exists_review.count() <= 0:
            review.save()
            return JsonResponse(dict(success=True))
        else:
            return JsonResponse({
                'success': False,
                'message': 'Review is already exist',
                'url': reverse('shops:update_review', kwargs={'slug': slug, 'pk': exists_review.first().id})
            })

    return JsonResponse(dict(success=False, message='Request is not AJAX!'))


@login_required
def update_shop_review(request, pk, slug):
    review = ShopReviews.objects.get(pk=pk)
    shop = Shop.objects.get(slug=slug)
    if request.POST:
        review.text = request.POST.get('text')
        review.shop = shop
        review.user = request.user
        if request.POST.get('rating'):
            review.stars = '*' * int(request.POST.get('rating'))
        review.save()
        return HttpResponseRedirect(shop.get_absolute_url())

    lenstars = len(review.stars)

    params = {
        'review': review,
        'object': Shop.objects.get(slug=slug),
        'lenstars': lenstars,
    }

    return render(request, 'shop/shop_review_update.html', params)


def shop_reviews(request):
    review = ShopReviews.objects.filter(shop__slug=request.POST.get('shop'))

    params = {
        'review': review
    }
    return render_to_response('layout/prod_reviews.html', params)
