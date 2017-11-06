import django_filters
from django import forms
from django.db.models import Q
from django import db

from apps.order.models import ORDER_STATUS_CHOICES


def search(queryset, name, value):
    db_type = db.connections.databases['default']['ENGINE']
    db_name = db_type.split(".")[-1]
    if db_name == 'mysql' or db_name == 'postgresql':
        return queryset.filter(Q(name__search=value) | Q(phone__search=value)).distinct()
    return queryset.filter(Q(name__icontains=value) | Q(phone__icontains=value)).distinct()


class OrderFilter(django_filters.FilterSet):
    created_at_from = django_filters.DateFilter(label='C', name='created_at', lookup_expr='gte')
    created_at_to = django_filters.DateFilter(label='До', name='created_at', lookup_expr='lte')
    status = django_filters.ChoiceFilter(label='Статус', choices=ORDER_STATUS_CHOICES)
    search = django_filters.CharFilter(label='Поиск',
                                       widget=forms.TextInput(attrs={'placeholder': 'Найти'}),
                                       method=search)
