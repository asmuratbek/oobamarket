import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, View, UpdateView, CreateView, DeleteView
from slugify import slugify

from apps.global_category.models import GlobalCategory
from apps.product.forms import ProductForm, ProductSearchForm, ShopSearchForm, ProductUpdateForm
from apps.properties.models import Values
from apps.users.mixins import AddProductMixin, DeleteProductMixin, UpdateProductMixin
from config.settings.base import MEDIA_ROOT
from .models import *


# Create your views here.


class UserFavoritesListView(LoginRequiredMixin, ListView):
    model = FavoriteProduct
    template_name = 'users/favorites.html'


# class ProductDetailView(DetailView):
#     model = Product


class FavoriteCreateView(LoginRequiredMixin, View):
    def get(self, request):
        item_id = request.GET.get("item")
        favorite, created = FavoriteProduct.objects.get_or_create(product_id=item_id, user=request.user)
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


def product_detail(request, global_slug, category_slug, slug):
    product = get_object_or_404(Product, slug=slug)
    category = get_object_or_404(Category, slug=category_slug)
    global_category = get_object_or_404(GlobalCategory, slug=global_slug)
    template = "product/product_detail.html"
    context = {
        "object": product
    }
    return render(request, template, context)


class ProductCreateView(LoginRequiredMixin, AddProductMixin, CreateView):
    form_class = ProductForm
    template_name = 'product/product_form.html'



    def get_success_url(self):
        return reverse('shops:detail', args=(self.object.shop.slug,))

    def get_initial(self):
        return {'shop': Shop.objects.get(slug=self.kwargs['slug']),
                'user': self.request.user
                }

    def form_valid(self, form, **kwargs):
        product = form.instance
        product.slug = slugify(form.instance.title)
        product.shop = Shop.objects.get(slug=self.kwargs['slug'])
        product.save()
        for key, value in self.request.POST.items():
            if key.startswith('property'):
                # property_id = key.split('-')[-1]
                value = get_object_or_404(Values, id=int(value))
                value.products.add(product)
        if form.cleaned_data['uploaded_images']:
            if ',' in form.cleaned_data['uploaded_images']:
                for item in form.cleaned_data['uploaded_images'].split(','):
                    try:
                        product_image = ProductImage.objects.get(id=int(item))
                        product_image.product = product
                        product_image.save()
                    except ObjectDoesNotExist:
                        pass
            else:
                try:
                    product_image = ProductImage.objects.get(id=int(form.cleaned_data['uploaded_images']))
                    product_image.product = product
                    product_image.save()
                except ObjectDoesNotExist:
                    print('error')
        form.save()
        if form.cleaned_data['removed_images']:
            for item in form.cleaned_data['removed_images'].split(','):
                try:
                    product_image = ProductImage.objects.get(id=int(item))
                    image_path = MEDIA_ROOT + '/' + product_image.image.name
                    os.remove(image_path)
                    product_image.delete()
                except ObjectDoesNotExist:
                    pass

        return super(ProductCreateView, self).form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateProductMixin, UpdateView):
    model = Product
    form_class = ProductUpdateForm
    template_name = 'product/product_update.html'

    def get_initial(self):
        initial = super(ProductUpdateView, self).get_initial()
        initial['user'] = self.request.user
        initial['parent_categories'] = self.object.category.parent.id
        initial['section'] = self.object.category.section.id
        return initial

    def get_form_kwargs(self):
        kwargs = super(ProductUpdateView, self).get_form_kwargs()
        return kwargs


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
    product_form = ProductSearchForm(request.GET)
    shop_form = ShopSearchForm(request.GET)
    products = product_form.search()
    shops = shop_form.search()
    template = 'search/home_page_search.html'
    return render(request, template, {
        'products': products,
        'shops': shops,
        'query': request.GET.get('q')
    })


def search(request):
    product_form = ProductSearchForm(request.GET)
    shop_form = ShopSearchForm(request.GET)
    products = product_form.search()
    for product in products:
        print(product.favorite)
    shops = shop_form.search()
    template = 'pages/search_results.html'
    return render(request, template, {
        'products': products,
        'shops': shops
    })


class ProductDeleteView(LoginRequiredMixin, DeleteProductMixin, DeleteView):
    model = Product
    template_name = 'layout/modal_product_delete_confirm.html'

    def get_success_url(self):
        return reverse("shops:detail", kwargs={'slug': self.object.shop.slug})


def change_publish_status(request):
    product = get_object_or_404(Product, id=request.GET.get('item'))
    if product.published:
        product.published = False
    else:
        product.published = True
    product.save()
    data = {
        "item": product.id,
        "message": "Продукт успешно опубликован" if product.published else "Продукт успешно скрыт"
    }
    return JsonResponse(data)
