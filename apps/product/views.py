import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from django.views.generic import ListView, View
from django.views.generic import UpdateView
from slugify import slugify

from apps.global_category.models import GlobalCategory
from apps.product.forms import ProductForm, ProductSearchForm, ShopSearchForm
from apps.users.mixins import AddProductMixin
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


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_update.html'

    def get_initial(self):
        return {
            'user': self.request.user
        }

# def create_new_ad(request):
#     form = AdCreationForm(request.POST, files=request.FILES)
#     if request.POST:
#         if form.is_valid():
#             new_ad = Ad()
#             new_ad.title = form.cleaned_data['title']
#             new_ad.description = form.cleaned_data['description']
#             new_ad.category = form.cleaned_data['category']
#             new_ad.city = form.cleaned_data['city']
#             new_ad.metro = form.cleaned_data['metro']
#             new_ad.phone = form.cleaned_data['phone']
#             new_ad.user = request.user if request.user and not request.user.is_anonymous else None
#             new_ad.price = form.cleaned_data['price'] if form.cleaned_data['price'] else 'Договорная'
#             temp_location = json.loads(form.cleaned_data['location'])
#             location = Coordinates()
#             position = Geoposition(temp_location['lat'], temp_location['lng'])
#             location.position = position
#             location.save()
#             new_ad.location = location
#             new_ad.is_active = True
#             new_ad.save()
#
#            if form.cleaned_data['removed_images']:
#                 removed_images = form.cleaned_data['removed_images'].split(',')
#                 for item in removed_images:
#                     try:
#                         r_media = Media.objects.get(id=int(item))
#                         file_path = settings.MEDIA_ROOT + '/' + r_media.media_file.name
#                         os.remove(file_path)
#                         r_media.delete()
#                     except ObjectDoesNotExist:
#                         pass
#
#            if form.cleaned_data['images']:
#                 images = form.cleaned_data['images'].split(',')
#                 for item in images:
#                     try:
#                         media = Media.objects.get(id=int(item))
#                         new_ad.media.add(media)
#                     except ObjectDoesNotExist:
#                         pass
#
#            link_to_ad = SITE_PROTOCOL + SITE_URL + '/admin/ad_app/ad/' + str(new_ad.id) + '/change'
#             message = '<b>Пользователь:</b>' + str(new_ad.user) if new_ad.user else '<b>Пользователь:</b> Аноним'
#             message += '<br>' + '<b>Дата:</b>' + str(
#                 datetime.date.today()) + '<br>' + '<b>Ссылка:</b> <a href="' + link_to_ad + '" target="_blank">' + link_to_ad + '</a>'
#             thread = threading.Thread(target=send_email_notification, args=('Новое объявление',
#                                                                             mark_safe(message),
#                                                                             ADMIN_EMAIL))
#             thread.start()
#             return HttpResponseRedirect(reverse('ad:one_ad', kwargs={'ad_id': new_ad.id}))
#         else:
#             print form.errors
#             return HttpResponseRedirect(reverse('index'))
#
#    return HttpResponseRedirect(reverse('index'))

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


class SearchResultsView(ListView):
    model = Product
    template_name = 'pages/search_results.html'

    def post(self, request, *args, **kwargs):
        import operator
        from django.db.models import Q
        from functools import reduce

        query = request.POST.get('keyword')
        if query:
            query_list = query.split()
            result = self.get_queryset().filter(
                reduce(operator.and_,
                       (Q(title__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(short_description__icontains=q) for q in query_list))
            )
        return result
