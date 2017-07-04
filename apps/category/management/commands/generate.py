import random

from django.core.management.base import BaseCommand, CommandError
from slugify import slugify
from django.db.utils import IntegrityError
from apps.category.models import Category
from apps.global_category.models import GlobalCategory
from django.conf import settings
import openpyxl as px
import string

from apps.properties.models import Properties


class Command(BaseCommand):
    help = 'Creates model instances from xlsx'

    def handle(self, *args, **options):
        W = px.load_workbook(settings.MEDIA_ROOT + '/ooba.xlsx')
        wiki = dict()
        first_level = list()
        second_level = list()
        third_level = list()
        second_level_props = list()
        third_level_props = list()
        values = list()
        for index, worksheet in enumerate(W.worksheets[1:3]):
            if index == 0:
                for row in worksheet.iter_rows():
                    for index, field in enumerate(row):
                        if field.value:
                            if index == 0:
                                key = field.value
                                wiki[key] = []
                            else:
                                wiki[key].append(field.value)

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
                                    category_level = str(field.internal_value).split('.')[-1][:2] if \
                                        str(field.internal_value).split('.')[-1][:2].isdigit() else \
                                        str(field.internal_value).split('.')[-1][0]
                                    if category_level:
                                        ids.append(category_level)
                                    second_level.append([ids, category_text])
                                else:
                                    property_text = str(field.internal_value).split('.')[-1].strip()
                                    second_level_props.append([ids, property_text])
                                    for column in string.ascii_uppercase[string.ascii_uppercase.find(field.column) + 1:]:
                                        if worksheet[column + str(field.row)].value:
                                            if str(worksheet[column + str(field.row)].value).startswith('Wiki'):
                                                key = str(worksheet[column + str(field.row)].value)[7:]
                                                if key in wiki.keys():
                                                    values.append([ids, property_text, wiki[key]])
                                            else:
                                                values.append([ids, property_text, worksheet[column + str(field.row)].value])

                    elif index == 2:
                        for index, field in enumerate(col):
                            if field.value and not str(field.internal_value).startswith('('):
                                if field.font.bold:
                                    ids = str(field.internal_value).split('.')[:-1]
                                    category_text = str(field.internal_value).split('.')[-1][2:].strip()
                                    category_level = str(field.internal_value).split('.')[-1][:2] if \
                                    str(field.internal_value).split('.')[-1][:2].isdigit() else \
                                    str(field.internal_value).split('.')[-1][0]
                                    if category_level:
                                        ids.append(category_level)
                                    third_level.append([ids, category_text])
                                else:
                                    property_text = str(field.internal_value).split('.')[-1].strip()
                                    third_level_props.append([ids, property_text])
                                    for column in string.ascii_uppercase[string.ascii_uppercase.find(field.column) + 1:]:
                                        if worksheet[column + str(field.row)].value:
                                            if str(worksheet[column + str(field.row)].value).startswith('Wiki'):
                                                key = str(worksheet[column + str(field.row)].value)[7:]
                                                if key in wiki.keys():
                                                    values.append([ids, property_text, wiki[key]])
                                            else:
                                                values.append([ids, property_text, worksheet[column + str(field.row)].value])

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
                        try:
                            title = sec_lvl_cat[-1]
                            slug = slugify(title)
                            sec_cat, created = Category.objects.get_or_create(title=title, slug=slug, parent=cat, section=section)
                            if created:
                                self.stdout.write(self.style.SUCCESS('Создана категория 2-ого уровня "%s"' % title))
                            else:
                                self.stdout.write(self.style.ERROR('{} уже существует'.format(title)))
                        except IntegrityError:
                            title = sec_lvl_cat[-1]
                            random_int = random.randrange(0, 101)
                            slug = slugify(title) + str(random_int)
                            sec_cat, created = Category.objects.get_or_create(title=title, slug=slug, parent=cat,
                                                                              section=section)
                            if created:
                                self.stdout.write(self.style.SUCCESS('Создана категория 2-ого уровня "%s"' % title))
                            else:
                                self.stdout.write(self.style.ERROR('{} уже существует'.format(title)))

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

                        for thrd_lvl_cat in third_level:
                            if sec_lvl_cat[0] == thrd_lvl_cat[0][:-1]:
                                try:
                                    title = thrd_lvl_cat[-1]
                                    random_int = random.randrange(0, 101)
                                    slug = slugify(title) + str(random_int)
                                    thrd_cat, created = Category.objects.get_or_create(title=title, slug=slug, parent=sec_cat, section=section)
                                    if created:
                                        self.stdout.write(self.style.SUCCESS('Создана категория 3-ого уровня "%s"' % title))
                                    else:
                                        self.stdout.write(self.style.ERROR('{} уже существует'.format(title)))
                                except IntegrityError:
                                    title = thrd_lvl_cat[-1]
                                    slug = slugify(title)
                                    thrd_cat, created = Category.objects.get_or_create(title=title, slug=slug,
                                                                                       parent=sec_cat, section=section)
                                    if created:
                                        self.stdout.write(
                                            self.style.SUCCESS('Создана категория 3-ого уровня "%s"' % title))
                                    else:
                                        self.stdout.write(self.style.ERROR('{} уже существует'.format(title)))

                                for prop in third_level_props:
                                    if prop[0] == thrd_lvl_cat[0]:
                                        title = prop[-1]
                                        if title.startswith('Wiki'):
                                            title = title[7:]
                                        slug = slugify(title)
                                        thrd_prop, created = Properties.objects.get_or_create(title=title,
                                                                                             slug=slug)
                                        thrd_prop.category.add(sec_cat)
                                        if created:
                                            self.stdout.write(
                                                self.style.SUCCESS('Создано свойство "%s"' % title))
                                        else:
                                            self.stdout.write(
                                                self.style.SUCCESS('Изменено свойство "%s"' % title))


                # for lev in first_level:
                #     for sec_lvl in second_level:
                #         if sec_lvl[0][0] == lev[0][0]:
                #             lev.append(sec_lvl[-1])
                    # category.append(i[-1] for i in second_level if second_level[0][0] == lev[0])
                    # for i in second_level:
                    #     print(i[-1])
                    # print(lev)
                # cat = dict((key, value) for (key, value) in first_level)
                # print(second_level)
                # print(first_level)
                # print(third_level_props)
                # print(values)
                # print(wiki)
                # print(category)
                # for i in second_level:
                #     print(i)
            #  field.value.split('.')[-1][0]
            # slug = slugify(worksheet.title)
            # section, created = GlobalCategory.objects.get_or_create(title=worksheet.title, slug=slug)
            # worksheet = W.get_sheet_by_name(name=worksheet.title)
            # for row in worksheet.iter_rows(max_col=1):
            #     for field in row:
            #         if field.internal_value:
            #             if field.internal_value[0].isdigit():
            #                 try:
            #                     title = field.internal_value[3:]
            #                     slug = slugify(title)
            #                     Category.objects.create(title=title, slug=slug, section=section)
            #                     self.stdout.write(self.style.SUCCESS('Создана категория-родитель "%s"' % title))
            #                 except IntegrityError:
            #                     title = field.internal_value[3:]
            #                     random_int = random.randrange(0, 101)
            #                     slug = slugify(title) + str(random_int)
            #                     Category.objects.create(title=title, slug=slug, section=section)
            #                     self.stdout.write(self.style.SUCCESS('Создана категория-родитель "%s"' % title))
            #             else:
            #                 try:
            #                     parents = Category.objects.filter(parent=None).order_by('created_at')
            #                     last_parent = parents.last()
            #                     slug = slugify(field.internal_value) + '-' + str(last_parent.id)
            #                     Category.objects.create(title=field.internal_value, slug=slug, section=section, parent=last_parent)
            #                     self.stdout.write(self.style.SUCCESS('Создана категория "%s"' % field.internal_value))
            #                 except IntegrityError:
            #                     parents = Category.objects.filter(parent=None).order_by('created_at')
            #                     last_parent = parents.last()
            #                     random_int = random.randrange(0, 1010)
            #                     slug = slugify(field.internal_value) + '-' + str(last_parent.id)
            #                     Category.objects.create(title=field.internal_value, slug=slug, section=section,
            #                                             parent=last_parent)
            #                     self.stdout.write(self.style.SUCCESS('Создана категория "%s"' % field.internal_value))


"""
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
                                self.stdout.write(self.style.SUCCESS('Создана категория "%s"' % field.internal_value))"""



# def parse_all_file():
#     file_load = px.load_workbook(settings.MEDIA_ROOT + "/" + 'categories.xlsx')
#     for worksheet in file_load.worksheets[1:]:
#         slug = slugify(worksheet.title)
#         section = GlobalCategory.objects.get_or_create(title=worksheet.title, slug=slug)
#         worksheet = file_load.get_sheet_by_name(name=worksheet.title)
#         for row in worksheet.iter_rows('A{}:A{}'.format(worksheet.min_row, worksheet.max_row)):
#             for field in row:
#                 if field.internal_value is not None and isinstance(field.internal_value[0], int):
#                     try:
#                         title = field.internal_value[3:]
#                         slug = slugify(title)
#                         Category.objects.create(title=title, slug=slug, section=section)
#                         print("Создана категория-родитель %s" % title)
#                         # self.stdout.write(self.style.SUCCESS('Создана категория-родитель "%s"' % title))
#                     except IntegrityError:
#                         title = field.internal_value[3:]
#                         random_int = random.randrange(0, 101)
#                         slug = slugify(title) + str(random_int)
#                         Category.objects.create(title=title, slug=slug, section=section)
#                         print("Создана категория-родитель %s" % title)
#                         # self.stdout.write(self.style.SUCCESS('Создана категория-родитель "%s"' % title))
