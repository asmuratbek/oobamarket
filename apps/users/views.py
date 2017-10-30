from allauth.account.models import EmailAddress
from allauth.account.views import EmailView
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, View
from django.db import IntegrityError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from apps.shop.models import Shop
from .models import User, Subscription
from .mixins import UserPermMixin


class UserDetailView(LoginRequiredMixin, UserPermMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'users/user_form.html')

    def post(self, request, *args, **kwargs):
        user = self.request.user
        email = self.request.POST.get('email', '')
        if self.request.POST.get('only_email'):
            if '@' not in email:
                return JsonResponse(dict(message='Введите павильный email', status=2))
            try:
                email_address = EmailAddress.objects.create(user=self.request.user, email=email)
            except IntegrityError:
                return JsonResponse(dict(status=1, message="Такой email уже существует."))
            email_count = user.emailaddress_set.count()
            message = "Email успешно добавлен"
            data = dict(emailaddress=email_address.email, email_count=email_count, message=message, status=0)
            return JsonResponse(data)
        elif self.request.POST.get('remove'):
            if user.emailaddress_set.count() == 1:
                message = "Вы не можете удалить единственный email."
                return JsonResponse(dict(message=message, status=1))
            email_address = get_object_or_404(EmailAddress, email=email)
            if email_address.primary is True:
                next_email = user.emailaddress_set.exclude(email=email).first()
                next_email.primary = True
                next_email.save()
            email_address.delete()
            data = dict(message='{} успешно удален.'.format(email), status=0)
            return JsonResponse(data)
        else:
            userform = get_object_or_404(User, username=kwargs['username'])
            if self.request.POST.get('username') is None or self.request.POST.get('username') == "":
                message = "Поле username не может быть пустым."
                messages.add_message(self.request, messages.ERROR, message)
                return HttpResponseRedirect(reverse('users:detail', kwargs={'username': user.username}))
            userform.username = self.request.POST.get('username', '')
            userform.first_name = self.request.POST.get('first_name', '')
            userform.phone = self.request.POST.get('phone', '')
            userform.last_name = self.request.POST.get('last_name', '')
            userform.address = self.request.POST.get('address', '')
            userform.save()
            if email:
                email_address = get_object_or_404(EmailAddress, email=email)
                email_address.primary = True
                email_address.save()
            return HttpResponseRedirect(reverse('users:detail', kwargs={'username': user.username}))


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
    msg = "Для того чтобы подписаться вам необходимо зарегистрироваться."
    messages.add_message(request, messages.INFO, msg)
    return HttpResponse('redirect')


class SubscribeListView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        from django.core.paginator import Paginator

        user = self.request.user
        sub_list = list()
        for sub in user.subscription_set.all():
            if sub.subscription_type == 'only_actions':
                [sub_list.append(item) for item in sub.subscription.sales_set.all().order_by("created_at")]
            elif sub.subscription_type == 'only_products':
                [sub_list.append(item) for item in sub.subscription.product_set.all().order_by("created_at")]
            else:
                [sub_list.append(item) for item in sub.subscription.sales_set.all().order_by("created_at")]
                [sub_list.append(item) for item in sub.subscription.product_set.all().order_by("created_at")]
        sorted_list = sorted(sub_list, key=lambda x: x.created_at, reverse=True)
        p = Paginator(sorted_list, 8)
        pages_count = p.num_pages
        page = self.request.GET.get('page')
        if page and int(page) <= pages_count:
            p = p.page(int(page))
            return render(self.request, 'users/subs.html', {'sub_objects': p.object_list})
        else:
            return render(self.request, 'users/subs.html', {})

    def get(self, request, *args, **kwargs):
        return render(self.request, 'users/sub_list.html', {})


