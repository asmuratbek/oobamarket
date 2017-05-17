from model_mommy import mommy
from django.core.management.base import BaseCommand
from apps.product.models import Product

class Command(BaseCommand):
    help = "My shiny new management command."

    # def add_arguments(self, parser):
    #         parser.add_argument('dummy-data', nargs='+')

    def handle(self, *args, **options):
        # raise NotImplementedError()
        print('hello')

    def add_products(self):
        pass