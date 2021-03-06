import os
import random, json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, render_to_response
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, View, UpdateView, CreateView, DeleteView
from slugify import slugify

from apps.global_category.models import GlobalCategory
from apps.product.forms import ProductForm, ProductUpdateForm, ProductImagesForm
from apps.properties.models import Values, Properties
from apps.reviews.forms import ProductReviewsForm
from apps.reviews.models import ProductReviews
from apps.utils.views import get_usd_currency
from decimal import Decimal
from apps.users.mixins import AddProductMixin, DeleteProductMixin, UpdateProductMixin
from config.settings.base import MEDIA_ROOT
from .models import *


# Create your views here.


class UserFavoritesListView(LoginRequiredMixin, ListView):
    model = FavoriteProduct
    template_name = 'users/favorites.html'


class FavoriteCreateView(LoginRequiredMixin, View):
    def get(self, request):
        item_id = request.GET.get("item")
        if item_id:
            favorite, created = FavoriteProduct.objects.get_or_create(product_id=item_id, user=request.user)
        else:
            return JsonResponse({
                "status": "error",
                "message": "item query param is required"
            })
        if not created:
            favorite.delete()
            flash_message = "Продукт успешно удален из избранных"
        else:
            flash_message = "Продукт успешно добавлен в избранное"
        favorites_count = request.user.get_favorites_count()
        data = {
            "created": created,
            "favorites_count": favorites_count,
            "flash_message": flash_message
        }
        return JsonResponse(data)


class ProductListView(ListView):
    model = Product
    template_name = 'product/all_products.html'


class ProductDetailView(generic.DetailView):
    model = Product
    template = 'product/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.kwargs
        request = self.request

        product = get_object_or_404(Product, slug=kw['slug'])

        get_object_or_404(Category, slug=kw['category_slug'])
        get_object_or_404(GlobalCategory, slug=kw['global_slug'])

        reviews = product.productreviews_set.all().order_by('-created_at')
        current_user = request.user

        context['form'] = ProductReviewsForm()

        if current_user.is_authenticated():
            user_review = product.productreviews_set.filter(user=current_user).first()

            if user_review is not None:
                context['already_added'] = True
                context['user_review'] = user_review
                context['form'] = ProductReviewsForm(instance=user_review, initial=dict(rating=len(user_review.stars)))

        context['reviews'] = reviews
        context['object'] = product
        context['global_slug'] = kw['global_slug']
        context['subscribe_shops'] = [sub.subscription.id for sub in request.user.subscription_set.all()] if request.user.is_authenticated else None

        return context


@login_required
def add_product_review(request, slug):
    if request.is_ajax():
        review = ProductReviews()
        review.text = request.POST.get('text')
        review.product = Product.objects.get(slug=slug)
        review.user = request.user
        if request.POST.get('rating'):
            review.stars = '*' * int(request.POST.get('rating'))

        review.save()
        return JsonResponse(dict(success=True))

    return JsonResponse(dict(success=False, message='Request is not AJAX!'))


@login_required
def update_product_review(request, pk, slug):
    review = ProductReviews.objects.get(pk=pk)
    product = Product.objects.get(slug=slug)

    if request.is_ajax():
        review.text = request.POST.get('text')
        review.product = product
        review.user = request.user
        if request.POST.get('rating'):
            review.stars = '*' * int(request.POST.get('rating'))
        review.save()
        return JsonResponse(dict(success=True))

    return JsonResponse(dict(success=False, message='Request is not AJAX!'))


def product_reviews(request):
    review = ProductReviews.objects.filter(product__slug=request.POST.get('product'))

    params = {
        'review': review
    }
    return render_to_response('layout/prod_reviews.html', params)


class ProductCreateView(LoginRequiredMixin, AddProductMixin, CreateView):
    form_class = ProductForm
    template_name = 'product/product_form.html'

    def get_success_url(self):
        return reverse('shops:detail', args=(self.object.shop.slug,))

    def get_initial(self):
        initial = dict()
        initial['shop'] = Shop.objects.get(slug=self.kwargs['slug'])
        initial['user'] = self.request.user
        return initial

    def form_invalid(self, form):
        form.fields.get('title').widget.attrs['disabled'] = False
        form.fields.get('parent_categories').widget.attrs['disabled'] = False
        form.fields.get('category').widget.attrs['disabled'] = False
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form, **kwargs):
        random_int = random.randrange(0, 1010)
        product = form.instance
        if product.currency != 'som' and product.price:
            usd = Currency.objects.filter(currency_type=product.currency).last()
            price = product.price * usd.exchange_rate if usd else product.price
            product.price = price
            product.currency = 'som' if usd else product.currency
        product.slug = slugify(form.instance.title, max_length=32) + str(random_int)
        product.shop = Shop.objects.get(slug=self.kwargs['slug'])
        product.save()
        # for key, value in self.request.POST.items():
        #     if key.startswith('val'):
        #         my_value = get_object_or_404(Values, id=int(key[4:]))
        #         my_value.products.add(product)
        #     elif key.startswith('property') and '---' not in value:
        #         my_value = get_object_or_404(Values, id=int(value))
        #         my_value.products.add(product)
        #     elif key.startswith("man-") and value:
        #         my_value, created = Values.objects.get_or_create(value=value, properties_id=int(key[4:]))
        #         my_value.products.add(product)
        if self.request.FILES:
            avatar = self.request.FILES.get('avatar')
            images = self.request.FILES.getlist('image')
            if avatar:
                ProductImage.objects.create(product=form.instance, image=avatar, is_avatar=True)
            other_images = [ProductImage(product=form.instance, image=img) for img in images]
            ProductImage.objects.bulk_create(other_images)
        return super(ProductCreateView, self).form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateProductMixin, UpdateView):
    model = Product
    form_class = ProductUpdateForm
    template_name = 'product/product_update.html'

    def get_initial(self, **kwargs):
        initial = super(ProductUpdateView, self).get_initial()
        initial['user'] = self.request.user
        initial['parent_categories'] = self.object.category.get_root().id
        initial['section'] = self.object.category.section.id
        return initial

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        product = form.instance
        product.slug = slugify(product.title) + '-' + str(product.id)
        product.save()
        product.values_set.clear()
        # for key, value in self.request.POST.items():
        #     if key.startswith('val'):
        #         value = get_object_or_404(Values, id=int(key[4:]))
        #         value.products.add(product)
        #     elif key.startswith('property') and '---' not in value:
        #         value = get_object_or_404(Values, id=int(value))
        #         value.products.add(product)
        #     elif key.startswith("man-") and value:
        #         my_value, created = Values.objects.get_or_create(value=value, properties_id=int(key[4:]))
        #         my_value.products.add(product)
        if form.data.get("old_avatar"):
            old_img_id = int(form.data.get("old_avatar", ""))
            old_image = get_object_or_404(ProductImage, id=old_img_id)
            old_image.is_avatar = False
            old_image.save()
        if form.data.get("new_avatar"):
            image_id = int(form.data.get("new_avatar", ""))
            image = get_object_or_404(ProductImage, id=image_id)
            image.is_avatar = True
            image.save()
        if form.data.get("delete_images"):
            del_list = [int(i) for i in form.data.get("delete_images").split(",")]
            product.productimage_set.filter(id__in=del_list).delete()
        if self.request.FILES:
            avatar = self.request.FILES.get('avatar', '')
            images = self.request.FILES.getlist('image')
            if avatar:
                ProductImage.objects.create(product=product, image=avatar, is_avatar=True)
            other_images = [ProductImage(product=product, image=img) for img in images]
            ProductImage.objects.bulk_create(other_images)
        data = dict(category=product.category.slug, section=product.category.section.slug,
                    product_slug=product.slug)
        # response = super(ProductUpdateView, self).form_valid(form)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        context['properties'] = self.object.category.properties_set.all()
        context['values'] = [val.id for val in self.object.values_set.all()]
        return context


class ProductIndexCreateView(LoginRequiredMixin, AddProductMixin, CreateView):
    template_name = 'product/product_form.html'

    def get_form_class(self):
        return ProductForm

    def get_success_url(self):
        return reverse('shops:detail', args=(self.object.shop.slug,))

    def get_initial(self):
        return {'user': self.request.user}

    def form_valid(self, form, **kwargs):
        form.instance.slug = slugify(form.instance.title)
        form.save()
        return super(ProductIndexCreateView, self).form_valid(form)


def upload_images(request):
    if request.method == 'POST':
        result = list()
        image_count = len(request.FILES)
        for i in range(0, image_count):
            image_file = request.FILES.get('file-' + str(i))
            media = ProductImage()
            media.image = image_file
            media.save()
            result.append({'id': media.id, 'url': media.image.url})

        return JsonResponse(dict(uploaded_files=result))
    return HttpResponseBadRequest


def remove_uploaded_image(request):
    if request.method == 'POST':
        ids = request.POST.get('media_ids')
        if ids:
            for item in ids.split(","):
                try:
                    r_media = ProductImage.objects.get(id=int(item))
                    image_path = MEDIA_ROOT + '/' + r_media.image.name
                    os.remove(image_path)
                    r_media.delete()
                except ObjectDoesNotExist:
                    pass

            return JsonResponse(dict(done=True))
        return JsonResponse(dict(done=False))
    return JsonResponse(dict(done=False))


def search_predict_html(request):
    q = request.GET.get('q')
    products = Product.objects.filter(
        Q(title__icontains=str(q))
    ).distinct()
    shops = Shop.objects.filter(
        Q(title__icontains=str(q))
    ).distinct()
    template = 'search/home_page_search.html'
    return render(request, template, {
        'products': products,
        'shops': shops,
        'query': request.GET.get('q')
    })


def search(request):
    q = request.POST.get('q')
    return render(request, 'search/search.html', {'q': q})


class ProductDeleteView(LoginRequiredMixin, DeleteProductMixin, DeleteView):
    model = Product
    template_name = 'layout/modal_product_delete_confirm.html'

    def get_success_url(self):
        return reverse("shops:detail", kwargs={'slug': self.object.shop.slug})


def change_publish_status(request):
    product = get_object_or_404(Product, id=request.GET.get('item'))
    if request.user.is_authenticated:
        is_owner = product.shop.is_owner(request.user)
        if not is_owner:
            status = "error"
            message = "Вы не можете изменять чужой продукт"
            return JsonResponse({
                "message": message,
                "status": status
            })
        message = ""
        if product.published:
            message = "Продукт успешно скрыт"
            product.published = False

        else:
            message = "Продукт успешно опубликован"
            product.published = True
        product.save()
        status = "success"
    else:
        status = "error"
        message = "Вы не можете изменять чужой продукт"
    data = {
        "item": product.id,
        "status": status,
        "published": product.published,
        "message": message
    }
    return JsonResponse(data)


@login_required
@csrf_exempt
def delete_product(request, slug):
    if request.method == "POST" and request.is_ajax():
        try:
            product = Product.objects.get(slug=slug)

            if request.user not in product.shop.user.all():
                return JsonResponse(dict(success=False,
                                         message='Товар не принадлежит текущему пользователю'))

            product.delete()
            return JsonResponse(dict(
                success=True, message='Товар успешно удален'
            ))
        except Product.DoesNotExist:
            return JsonResponse(dict(
                success=False, message='Товар не найден'
            ))
    else:
        return HttpResponseBadRequest


@login_required
@csrf_exempt
def upload_images_product_update(request, slug):
    if request.method == "POST" and request.is_ajax():
        form = ProductImagesForm(request.POST, request.FILES)
        if form.is_valid():
            product = get_object_or_404(Product, slug=slug)
            form.instance.product = product
            product_image = form.save()
            data = {'is_valid': True, 'productimage_id': product_image.id, 'name': product_image.image.name,
                    'url': product_image.image.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)
    return HttpResponseBadRequest


@login_required
@csrf_exempt
def delete_product_images(request):
    if request.method == 'POST' and request.is_ajax():
        product_image_id = request.POST.get('productimage_id', '')
        if product_image_id:
            product = get_object_or_404(ProductImage, id=product_image_id)
            product.delete()
            return JsonResponse({'status': 0, 'message': 'Productimage is succefully delete.'})
        return JsonResponse({'status': 1, 'message': 'Product_image_id field must not be null.'})
    return JsonResponse({'status': 2, 'message': 'Request must be post.'})
