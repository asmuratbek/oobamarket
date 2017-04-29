from django.views import generic
from apps.category.models import Category


class CategoryDetailView(generic.DetailView):
    model = Category



