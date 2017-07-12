import random

from django.core.management.base import BaseCommand, CommandError
from slugify import slugify
from django.db.utils import IntegrityError
from apps.category.models import Category
from apps.global_category.models import GlobalCategory
from django.conf import settings
import openpyxl as px
import string

from apps.properties.models import Properties, Values


class Command(BaseCommand):
    help = 'Creates model instances from xlsx'

    def handle(self, *args, **options):
        W = px.load_workbook(settings.DUMP_ROOT + '/ooba.xlsx')
        wiki = dict()
        first_level = list()
        second_level = list()
        third_level = list()
        second_level_props = list()
        third_level_props = list()
        values = list()
        for index, worksheet in enumerate(W.worksheets[1:5]):
            if index == 0:
                for row in worksheet.iter_rows():
                    for index, field in enumerate(row):
                        if field.value:
                            if index == 0:
                                key = field.value
                                wiki[key] = []
                            else:
                                wiki[key].append(str(field.value).capitalize())

            else:
                slug = slugify(worksheet.title)
                section, created = GlobalCategory.objects.get_or_create(title=worksheet.title, slug=slug)
                for index, col in enumerate(worksheet.iter_cols(max_col=3)):
                    if index == 0:
                        for index, field in enumerate(col):
                            if field.value:
                                first_level.append([str(field.internal_value).split('.')[:-1], str(field.internal_value).split('.')[-1][1:]])

                    elif index == 1:
                        for index, field in enumerate(col):
                            if field.value and not str(field.value).startswith('('):
                                if field.font.bold:
                                    ids = str(field.internal_value).split('.')[:-1]
                                    category_text = str(field.internal_value).split('.')[-1][2:].strip()
                                    category_text = category_text.capitalize()
                                    category_level = str(field.internal_value).split('.')[-1][:2] if \
                                        str(field.internal_value).split('.')[-1][:2].isdigit() else \
                                        str(field.internal_value).split('.')[-1][0]
                                    if category_level:
                                        ids.append(category_level)
                                    second_level.append([ids, category_text])
                                else:
                                    property_text = str(field.internal_value).split('.')[-1].strip()
                                    if property_text.startswith('**'):
                                        property_text = property_text[3:]
                                    elif property_text.startswith('*') or property_text.startswith("#") or property_text.startswith("!"):
                                        property_text = property_text[2:]
                                    property_text = property_text.capitalize()
                                    second_level_props.append([ids, property_text])
                                    for column in string.ascii_uppercase[string.ascii_uppercase.find(field.column) + 1:]:
                                        if worksheet[column + str(field.row)].value:
                                            if str(worksheet[column + str(field.row)].value).startswith('Wiki'):
                                                key = str(worksheet[column + str(field.row)].value)[7:]
                                                if key in wiki.keys():
                                                    values.append([ids, property_text, wiki[key]])
                                            else:
                                                if not str(worksheet[column + str(field.row)].value).startswith("("):
                                                    values.append([ids, property_text, str(worksheet[column + str(field.row)].value).capitalize()])

                    elif index == 2:
                        for index, field in enumerate(col):
                            if field.value and not str(field.internal_value).startswith('('):
                                if field.font.bold:
                                    ids = str(field.internal_value).split('.')[:-1]
                                    category_text = str(field.internal_value).split('.')[-1][2:].strip()
                                    category_text = category_text.capitalize()
                                    category_level = str(field.internal_value).split('.')[-1][:2] if \
                                    str(field.internal_value).split('.')[-1][:2].isdigit() else \
                                    str(field.internal_value).split('.')[-1][0]
                                    if category_level:
                                        ids.append(category_level)
                                    third_level.append([ids, category_text])
                                else:
                                    property_text = str(field.internal_value).split('.')[-1].strip()
                                    if property_text.startswith('**'):
                                        property_text = property_text[3:]
                                    elif property_text.startswith('*') or property_text.startswith("#") or property_text.startswith("!"):
                                        property_text = property_text[2:]
                                    property_text = property_text.capitalize()
                                    third_level_props.append([ids, property_text])
                                    for column in string.ascii_uppercase[string.ascii_uppercase.find(field.column) + 1:]:
                                        if worksheet[column + str(field.row)].value:
                                            if str(worksheet[column + str(field.row)].value).startswith('Wiki'):
                                                key = str(worksheet[column + str(field.row)].value)[7:]
                                                if key in wiki.keys():
                                                    values.append([ids, property_text, wiki[key]])
                                            else:
                                                if not str(worksheet[column + str(field.row)].value).startswith("("):
                                                    values.append([ids, property_text, str(worksheet[column + str(field.row)].value).capitalize()])

            for category in first_level:
                try:
                    title = category[-1]
                    slug = slugify(title)
                    cat, created = Category.objects.get_or_create(title=title, slug=slug, section=section)
                    if created:
                        self.stdout.write(self.style.SUCCESS('Создана категория 1-ого уровня "%s"' % title))
                    else:
                        self.stdout.write(self.style.ERROR('{} уже существует'.format(title)))
                except IntegrityError:
                    title = category[-1]
                    random_int = random.randrange(0, 101)
                    slug = slugify(title) + str(random_int)
                    cat, created = Category.objects.get_or_create(title=title, slug=slug, section=section)
                    if created:
                        self.stdout.write(self.style.SUCCESS('Создана категория 1-ого уровня "%s"' % title))
                    else:
                        self.stdout.write(self.style.ERROR('{} уже существует'.format(title)))

                for sec_lvl_cat in second_level:
                    if category[0][0] == sec_lvl_cat[0][0]:
                        title = sec_lvl_cat[-1]
                        possible_categories = Category.objects.filter(title=title, parent=cat, section=section)

                        if possible_categories:
                            self.stdout.write(self.style.ERROR('{} уже существует'.format(title)))
                            sec_cat = possible_categories.first()
                        else:
                            random_int = random.randrange(0, 101)
                            slug = slugify(title) + str(random_int)
                            sec_cat = Category.objects.create(title=title, slug=slug, parent=cat, section=section)
                            self.stdout.write(self.style.SUCCESS('Создана категория 2-ого уровня "%s"' % title))

                        for prop in second_level_props:
                            if prop[0] == sec_lvl_cat[0]:
                                title = prop[-1]
                                if title.startswith('Wiki'):
                                    title = title[7:]
                                slug = slugify(title)
                                sec_prop,created = Properties.objects.get_or_create(title=title, slug=slug)
                                sec_prop.category.add(sec_cat)
                                if created:
                                    self.stdout.write(self.style.SUCCESS('Создано свойство "%s"' % title))
                                else:
                                    self.stdout.write(self.style.SUCCESS('Изменено свойство "%s"' % title))

                                for val in values:
                                    if prop[0] == val[0]:
                                        value = val[-1]
                                        if sec_prop.title == val[1]:
                                            if isinstance(value, list):
                                                for v in value:
                                                    created_value, created = Values.objects.get_or_create(value=v,
                                                                                                          properties=sec_prop)
                                                    if created:
                                                        self.stdout.write(
                                                            self.style.SUCCESS('Создано значение "%s"' % v))
                                                    else:
                                                        self.stdout.write(
                                                            self.style.SUCCESS('Изменено значение "%s"' % v))
                                            else:
                                                created_value, created = Values.objects.get_or_create(value=value, properties=sec_prop)
                                                if created:
                                                    self.stdout.write(self.style.SUCCESS('Создано значение "%s"' % value))
                                                else:
                                                    self.stdout.write(self.style.SUCCESS('Изменено значение "%s"' % value))

                        for thrd_lvl_cat in third_level:
                            if sec_lvl_cat[0] == thrd_lvl_cat[0][:-1]:
                                title = thrd_lvl_cat[-1]
                                possible_categories = Category.objects.filter(title=title, parent=sec_cat, section=section)

                                if possible_categories:
                                    self.stdout.write(self.style.ERROR('{} уже существует'.format(title)))
                                    thrd_cat = possible_categories.first()
                                else:
                                    random_int = random.randrange(0, 101)
                                    slug = slugify(title) + str(random_int)
                                    thrd_cat = Category.objects.create(title=title, slug=slug, parent=sec_cat, section=section)
                                    self.stdout.write(self.style.SUCCESS('Создана категория 3-ого уровня "%s"' % title))

                                for prop in third_level_props:
                                    if prop[0] == thrd_lvl_cat[0]:
                                        title = prop[-1]
                                        if title.startswith('Wiki'):
                                            title = title[7:]
                                        slug = slugify(title)
                                        thrd_prop, created = Properties.objects.get_or_create(title=title,
                                                                                             slug=slug)
                                        thrd_prop.category.add(thrd_cat)
                                        if created:
                                            self.stdout.write(
                                                self.style.SUCCESS('Создано свойство "%s"' % title))
                                        else:
                                            self.stdout.write(
                                                self.style.SUCCESS('Изменено свойство "%s"' % title))

                                        for val in values:
                                            if prop[0] == val[0]:
                                                value = val[-1]
                                                if thrd_prop.title == val[1]:
                                                    if isinstance(value, list):
                                                        for v in value:
                                                            created_value, created = Values.objects.get_or_create(
                                                                value=v, properties=thrd_prop)
                                                            if created:
                                                                self.stdout.write(
                                                                    self.style.SUCCESS('Создано значение "%s"' % v))
                                                            else:
                                                                self.stdout.write(
                                                                    self.style.SUCCESS('Изменено значение "%s"' % v))
                                                    else:
                                                        created_value, created = Values.objects.get_or_create(value=value, properties=thrd_prop)
                                                        if created:
                                                            self.stdout.write(
                                                                self.style.SUCCESS('Создано значение "%s"' % value))
                                                        else:
                                                            self.stdout.write(
                                                                self.style.SUCCESS('Изменено значение "%s"' % value))

