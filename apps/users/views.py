from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, View

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from apps.shop.models import Shop
from .models import User, Subscription


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    fields = ['name', 'username', 'first_name', 'last_name']

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UsersFavoritesListView(DetailView):
    model = User
    template_name = 'users/favorites.html'


@csrf_exempt
def subscribe(request):
    if request.user.is_authenticated:
        if request.method == 'POST' and request.is_ajax():
            user = request.user
            shop_slug = request.POST.get('shop_slug', '')
            shop = get_object_or_404(Shop, slug=shop_slug)
            data = dict()
            if not request.POST.get('sub-type'):
                sub_obj, created = Subscription.objects.get_or_create(user=user, subscription=shop)
                if not created:
                    sub_obj.delete()
                    data['message'] = 'Вы отписаны от обновлений'
                    data['status'] = 0
                    return JsonResponse(data)
                data['message'] = 'Подписка оформлена'
                data['status'] = 1
                return JsonResponse(data)
            else:
                sub_type = request.POST.get('sub-type', '')
                try:
                    sub = Subscription.objects.get(user=user, subscription=shop)
                except Subscription.DoesNotExist:
                    return Http404
                sub.subscription_type = sub_type
                sub.save()
                data['message'] = 'Параметры подписки изменены'
                return JsonResponse(data)
        return HttpResponseBadRequest()
    return HttpResponse('redirect')


class SubscribeListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        sales = list()
        products = list()
        for sub in user.subscription_set.all():
            if sub.subscription_type == 'only_actions':
                [sales.append(item) for item in sub.subscription.sales_set.all()]
            elif sub.subscription_type == 'only_products':
                [products.append(item) for item in sub.subscription.product_set.all()]
            else:
                [sales.append(item) for item in sub.subscription.sales_set.all()]
                [products.append(item) for item in sub.subscription.product_set.all()]
        return render(self.request, 'users/sub_list.html', {'sales': sales,
                                                            'products': products})
