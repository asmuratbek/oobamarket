import random

from django.core.management.base import BaseCommand, CommandError
from slugify import slugify
from django.db.utils import IntegrityError
from apps.category.models import Category
from apps.global_category.models import GlobalCategory
from django.conf import settings
import openpyxl as px


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
                            except IntegrityError:
                                title = field.internal_value[3:]
                                random_int = random.randrange(0, 101)
                                slug = slugify(title) + str(random_int)
                                Category.objects.create(title=title, slug=slug, section=section)
                                self.stdout.write(self.style.SUCCESS('Создана категория-родитель "%s"' % title))
                        else:
                            try:
                                parents = Category.objects.filter(parent=None).order_by('created_at')
                                last_parent = parents.last()
                                slug = slugify(field.internal_value) + '-' + str(last_parent.id)
                                Category.objects.create(title=field.internal_value, slug=slug, section=section, parent=last_parent)
                                self.stdout.write(self.style.SUCCESS('Создана категория "%s"' % field.internal_value))
                            except IntegrityError:
                                parents = Category.objects.filter(parent=None).order_by('created_at')
                                last_parent = parents.last()
                                random_int = random.randrange(0, 1010)
                                slug = slugify(field.internal_value) + '-' + str(last_parent.id)
                                Category.objects.create(title=field.internal_value, slug=slug, section=section,
                                                        parent=last_parent)
                                self.stdout.write(self.style.SUCCESS('Создана категория "%s"' % field.internal_value))


def parse_all_file():
    file_load = px.load_workbook(settings.MEDIA_ROOT + "/" + 'categories.xlsx')
    for worksheet in file_load.worksheets[1:]:
        slug = slugify(worksheet.title)
        section = GlobalCategory.objects.get_or_create(title=worksheet.title, slug=slug)
        worksheet = file_load.get_sheet_by_name(name=worksheet.title)
        for row in worksheet.iter_rows('A{}:A{}'.format(worksheet.min_row, worksheet.max_row)):
            for field in row:
                if field.internal_value is not None and isinstance(field.internal_value[0], int):
                    try:
                        title = field.internal_value[3:]
                        slug = slugify(title)
                        Category.objects.create(title=title, slug=slug, section=section)
                        print("Создана категория-родитель %s" % title)
                        # self.stdout.write(self.style.SUCCESS('Создана категория-родитель "%s"' % title))
                    except IntegrityError:
                        title = field.internal_value[3:]
                        random_int = random.randrange(0, 101)
                        slug = slugify(title) + str(random_int)
                        Category.objects.create(title=title, slug=slug, section=section)
                        print("Создана категория-родитель %s" % title)
                        # self.stdout.write(self.style.SUCCESS('Создана категория-родитель "%s"' % title))
