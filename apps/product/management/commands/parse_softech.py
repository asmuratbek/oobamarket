import requests, re
import urllib.request
from functools import reduce
from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from django.http import Http404
from django.utils.html import strip_tags
from slugify import slugify
from xlwt import Workbook


class Command(BaseCommand):
    help = "Parse products from www.softech.kg"

    def handle(self, *args, **options):
        url = "https://softech.kg"
        html = requests.get(url).content
        soup = BeautifulSoup(html, "lxml")
        cats_block = soup.find("ul", class_="menu")
        cats_links = [li.find("a").get("href") for li in cats_block.find_all("li", class_=None)]
        # [cats_links.remove(li.find("a").get("href")) for li in cats_block.find_all("li", class_="children")]
        print(len(cats_links))
        print(cats_links)
