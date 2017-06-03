import random

from django.core.management.base import BaseCommand, CommandError
from slugify import slugify

from apps.category.models import Category
from apps.global_category.models import GlobalCategory
from django.conf import settings
import openpyxl as px
from multiprocessing import Pool

"""import openpyxl as px
import numpy as np

W = px.load_workbook('filename.xlsx', use_iterators = True)
p = W.get_sheet_by_name(name = 'Sheet1')

a=[]

for row in p.iter_rows():
    for k in row:
        a.append(k.internal_value)"""


class Command(BaseCommand):
    help = 'Creates model instances from xlsx'

    def add_arguments(self, parser):
        parser.add_argument('type', type=str)

    def handle(self, *args, **options):
        type = options['type']
        W = px.load_workbook(settings.MEDIA_ROOT + '/' + str(type) + '.xlsx')
        for worksheet in W.worksheets:
            slug = slugify(worksheet.title)
            section, created = GlobalCategory.objects.get_or_create(title=worksheet.title, slug=slug)
            print(worksheet.title)
            worksheet = W.get_sheet_by_name(name=worksheet.title)
            for row in worksheet.iter_rows(max_col=1):
                for field in row:
                    if field.internal_value:
                        if field.internal_value[0].isdigit():
                            try:
                                title = field.internal_value[3:]
                                slug = slugify(title)
                                Category.objects.create(title=title, slug=slug, section=section)
                                self.stdout.write(self.style.SUCCESS('Создана категория-родитель "%s"' % title))
                            except:
                                title = field.internal_value[3:]
                                random_int = random.randrange(0, 101)
                                slug = slugify(title) + str(random_int)
                                Category.objects.create(title=title, slug=slug, section=section)
                                self.stdout.write(self.style.SUCCESS('Создана категория-родитель "%s"' % title))
                        else:
                            try:
                                parents = Category.objects.filter(parent=None).order_by('created_at')
                                last_parent = parents.last()
                                slug = slugify(field.internal_value)
                                Category.objects.create(title=field.internal_value, slug=slug, section=section, parent=last_parent)
                                self.stdout.write(self.style.SUCCESS('Создана категория "%s"' % field.internal_value))
                            except:
                                parents = Category.objects.filter(parent=None).order_by('created_at')
                                last_parent = parents.last()
                                random_int = random.randrange(0, 1010)
                                slug = slugify(field.internal_value) + str(random_int)
                                Category.objects.create(title=field.internal_value, slug=slug, section=section,
                                                        parent=last_parent)
                                self.stdout.write(self.style.SUCCESS('Создана категория "%s"' % field.internal_value))
        # a = []
        #
        # for row in p.iter_rows():
        #     for k in row:
        #         a.append(k.internal_value)
        # file = open(settings.MEDIA_ROOT + '/' + str(type) + '.xlsx')
        # print(file)
        # for type in options['type']:
        #     try:
        #         poll = Category.objects.get(pk=type)
        #     except Category.DoesNotExist:
        #         raise CommandError('Poll "%s" does not exist' % type)
        #
        #     poll.opened = False
        #     poll.save()
        #
        #     self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % type))
