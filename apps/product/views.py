from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from django.views.generic import ListView, View
from django.views.generic import UpdateView
from slugify import slugify

from apps.global_category.models import GlobalCategory
from apps.product.forms import ProductForm, ProductSearchForm
from apps.users.mixins import AddProductMixin
from .models import *
from config.settings.base import MEDIA_ROOT
import os

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
        form.instance.slug = slugify(form.instance.title)
        form.instance.shop = Shop.objects.get(slug=self.kwargs['slug'])
        form.save()
        if form.cleaned_data['uploaded_images']:
            for item in form.cleaned_data['uploaded_images'].split(','):
                try:
                    media = Media.objects.get(id=int(item))
                    form.images.add(media)
                except ObjectDoesNotExist:
                    pass

        if form.cleaned_data['removed_images']:
            for item in form.cleaned_data['removed_images'].split(','):
                try:
                    media = Media.objects.get(id=int(item))
                    image_path = MEDIA_ROOT + '/' + media.image.name
                    os.remove(image_path)
                    media.delete()
                except ObjectDoesNotExist:
                    pass
        return super(ProductCreateView, self).form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_update.html'

    def get_initial(self):
        return {
            'user': self.request.user
        }


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
            media = Media()
            media.image = image_file
            media.save()
            result.append({'id':media.id, 'url':media.image.url})

        return JsonResponse(dict(uploaded_files=result))


def remove_uploaded_image(request):
    if request.method == 'POST':
        ids = request.POST.get('media_ids')
        if ids:
            for item in ids.split(","):
                try:
                    r_media = Media.objects.get(id=int(item))
                    image_path = MEDIA_ROOT+'/'+r_media.image.name
                    os.remove(image_path)
                    r_media.delete()
                except ObjectDoesNotExist:
                    pass

            return JsonResponse(dict(done=True))
        return JsonResponse(dict(done=False))
    return JsonResponse(dict(done=False))



def notes(request):
    form = ProductSearchForm(request.GET)
    notes = form.search()

    return render(request, 'search/search.html', {'notes': notes})


class SearchResultsView(ListView):
    model = Product
    template_name = 'pages/search_results.html'
