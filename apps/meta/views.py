from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView
from .models import Claim
from django.conf import settings
from django.contrib import messages
from .forms import ClaimForm
# Create your views here.


class ClaimCreate(CreateView):
    form_class = ClaimForm
    template_name = "layout/landing.html"

    def get(self, request, *args, **kwargs):
        return render(request, 'layout/landing.html')

    def form_invalid(self, form):
        msg = "Введеные вами данные не корректны."
        messages.add_message(self.request, messages.WARNING, msg)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        admin, email = settings.ADMINS[-1]
        name = form.cleaned_data.get("name")
        phone = form.cleaned_data.get("phone")
        message = "Новая заявка: \n Название магазина: {name}, \n Номер телефона: {phone} \n".format(name=name, phone=phone)
        send_mail("Ooba market", message, settings.EMAIL_HOST_USER, [email])
        msg = "Ваша заявка будет рассмотрена в ближайшее время."
        messages.add_message(self.request, messages.INFO, msg)
        return super(ClaimCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('home')
