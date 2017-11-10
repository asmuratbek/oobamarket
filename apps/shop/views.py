from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.urls import reverse
from django.utils.decorators import method_decorator
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
from apps.shop.forms import ShopForm, ShopBannersForm, ShopSocialLinksForm, ShopInlineFormSet, SalesCreateForm
from apps.users.mixins import ShopMixin
from .models import Shop, SocialLinks, Banners, Contacts, Sales, DAYS
import random
from apps.reviews.forms import ShopReviewsForm

# Create your views here.
class ShopListView(generic.ListView):
    model = Shop

    def get_context_data(self, **kwargs):
        context = super(ShopListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['subscribe_shops'] = [sub.subscription.id for sub in self.request.user.subscription_set.all()]
        return context


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


class LoginRequiredMixin1(AccessMixin):
    """
    CBV mixin which verifies that the current user is authenticated.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request,
                          'Для того чтобы создать магазин и добавить товар вам необходимо зарегистрироваться или войти.')
            return self.handle_no_permission()
        return super(LoginRequiredMixin1, self).dispatch(request, *args, **kwargs)


class ShopCreateView(LoginRequiredMixin1, FormsetMixin, CreateView):
    form_class = ShopForm
    formset_class = ShopInlineFormSet
    model = Shop
    template_name = 'shop/shop_form.html'

    def get_success_url(self):
        return reverse('shops:detail', args=(self.object.slug,))

    def get_context_data(self, **kwargs):
        context = super(ShopCreateView, self).get_context_data(**kwargs)
        context['days'] = DAYS
        return context

    def form_invalid(self, form, formset):
        messages.add_message(self.request, messages.WARNING, form.errors)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form, formset):
        random_int = random.randrange(0, 1010)
        form.instance.slug = slugify(form.instance.title, max_length=32) + str(random_int)
        self.object = form.save()
        form.instance.user.add(self.request.user)
        formset.instance = self.object
        formset.save()
        return super(ShopCreateView, self).form_valid(form, formset)


class ShopUpdateView(LoginRequiredMixin, FormsetMixin, ShopMixin, UpdateView):
    model = Shop
    is_update_view = True
    form_class = ShopForm
    formset_class = ShopInlineFormSet
    template_name = 'shop/shop_update.html'

    def get_context_data(self, **kwargs):
        context = super(ShopUpdateView, self).get_context_data(**kwargs)
        context['days'] = DAYS
        contact = self.object.contacts_set.first()
        if contact:
            context['longitude'] = contact.place.longitude if contact.place else contact.longitude
            context['latitude'] = contact.place.latitude if contact.place else contact.latitude
        else:
            context['longitude'] = ""
            context['latitude'] = ""
        return context

    def form_invalid(self, form, formset):
        messages.add_message(self.request, messages.WARNING, form.errors)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form, formset):
        form.save()
        formset.save()
        return super(ShopUpdateView, self).form_valid(form, formset)


class ShopDeleteView(LoginRequiredMixin, ShopMixin, DeleteView):
    model = Shop
    template_name = 'layout/modal_shop_delete_confirm.html'
    success_url = '/'



class ShopAboutUsDetailView(generic.DetailView):
    model = Shop
    template_name = 'shop/about-us.html'


class ShopSaleListView(generic.DetailView):
    model = Shop
    template_name = 'shop/sale.html'


class ShopSaleArchiveView(generic.DetailView):
    model = Shop
    template_name = 'shop/sale_archive.html'


def sale_detail(request, slug, pk):
    shop = get_object_or_404(Shop, slug=slug)
    sale = get_object_or_404(Sales, id=pk)
    print(sale)

    context = {
        'shop': shop,
        'sales': sale
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


class ShopReviewListView(generic.DetailView):
    model = Shop
    template_name = 'shop/shop_review.html'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['form'] = ShopReviewsForm()

        shop = kwargs['object']
        context['shop'] = shop
        context['reviews'] = shop.shopreviews_set.all().order_by('-created_at')

        current_user = self.request.user

        if current_user.is_authenticated():
            user_review = shop.shopreviews_set.filter(user=current_user).first()

            if user_review is not None:
                context['already_added'] = True
                context['user_review'] = user_review
                context['form'] = ShopReviewsForm(instance=user_review, initial=dict(rating=len(user_review.stars)))

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

        review.save()
        return JsonResponse(dict(success=True))

    return JsonResponse(dict(success=False, message='Request is not AJAX!'))


@login_required
def update_shop_review(request, pk, slug):
    review = ShopReviews.objects.get(pk=pk)
    shop = Shop.objects.get(slug=slug)
    if request.is_ajax():
        review.text = request.POST.get('text')
        review.shop = shop
        review.user = request.user
        if request.POST.get('rating'):
            review.stars = '*' * int(request.POST.get('rating'))
        review.save()
        return JsonResponse(dict(success=True))

    return JsonResponse(dict(success=False, message='Request is not AJAX!'))


def shop_reviews(request):
    review = ShopReviews.objects.filter(shop__slug=request.POST.get('shop'))

    params = {
        'review': review
    }
    return render_to_response('layout/shop_reviews.html', params)


class ShopContactsView(generic.DetailView):
    model = Shop
    template_name = 'shop/contacts.html'

    def get_context_data(self, **kwargs):
        context = super(ShopContactsView, self).get_context_data()
        contact = self.object.contacts_set.first()
        if contact:
            context['longitude'] = contact.place.longitude if contact.place else contact.longitude
            context['latitude'] = contact.place.latitude if contact.place else contact.latitude
        else:
            context['longitude'] = ""
            context['latitude'] = ""
        return context


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


class CreateBanners(LoginRequiredMixin, ShopMixin, View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CreateBanners, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        shop = get_object_or_404(Shop, slug=slug)
        banners = shop.banners_set.all()
        return render(self.request, 'shop/shop_banner.html', {'banners': banners,
                                                              'slug': slug})

    def post(self, request, *args, **kwargs):
        shop = get_object_or_404(Shop, slug=self.kwargs['slug'])
        images = request.FILES.getlist('image_file')
        delete_images = request.POST.get('delete_images')
        if images:
            images_list = [Banners(image=file, shop=shop) for file in images]
            Banners.objects.bulk_create(images_list)
        if delete_images:
            delete_list = Banners.objects.filter(id__in=delete_images.split(","))
            delete_list.delete()
        return JsonResponse({'status': 0, 'url': str(shop.get_absolute_url())})
        # else:
        #     print(len(request.FILES['image']))
        #     for file in request.FILES.getlist('image'):
        #         Banners.objects.create(title="", image=file, shop=shop)
        # return HttpResponseRedirect(shop.get_absolute_url())


class ShopBannerDeleteView(LoginRequiredMixin, ShopMixin, DeleteView):
    pass


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
