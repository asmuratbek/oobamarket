import requests, xlrd, xml.etree.ElementTree as ET
from django.core.management import BaseCommand
from apps.product.models import Currency
from decimal import Decimal


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            res = requests.get('http://www.nbkr.kg/XML/daily.xml', timeout=3)
        except (requests.ConnectionError, requests.ConnectTimeout):
            currency = Currency.objects.filter(currency_type='dollar').last()
            usd = currency.exchange_rate if currency else None
            print('Connection Error')
            return usd
        tree = ET.fromstring(res.content)
        usd_currency = [i for i in tree.findall('Currency[@ISOCode="USD"]')]
        usd = usd_currency[0].find('Value').text
        if usd:
            usd = usd.replace(",", ".")[:5]
            c_delete = Currency.objects.filter(currency_type='dollar').delete()
            c_create = Currency.objects.create(currency_type='dollar', exchange_rate=Decimal(usd))
            print("Currency is created")
