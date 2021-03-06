from django.shortcuts import render
# Create your views here.
from django.views import generic

from apps.global_category.models import GlobalCategory
from apps.product.models import Product
from apps.shop.models import Shop


class IndexView(generic.TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['shops'] = Shop.objects.all()[:12]
        if self.request.user.is_authenticated:
            context['subscribe_shops'] = [sub.subscription.id for sub in self.request.user.subscription_set.all()]
        context["weeks_best_products"] = Product.objects.all()[:12]
        return context


class GlobalDetailView(generic.DetailView):
    model = GlobalCategory

    def get_context_data(self, **kwargs):
        context = super(GlobalDetailView, self).get_context_data()
        context['global_slug'] = self.object.slug
        return context

def landing(request):
    return render(request, 'layout/landing.html')
