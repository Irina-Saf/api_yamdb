import csv

from django.core.management import BaseCommand
from api_yamdb.settings import CSV_FILES_DIR
from reviews.models import (
    Category,
    Comment,
    Genre,
    GenreTitle,
    Review,
    Title,
    User
)


FILES_CLASSES = {
    'category': Category,
    'genre': Genre,
    'titles': Title,
    'genre_title': GenreTitle,
    'users': User,
    'review': Review,
    'comments': Comment,
}

FIELDS = {
    'author': 'author_id',
    'category': 'category_id'
}


class Command(BaseCommand):

    def handle(self, *args, **options):
        for key, value in FILES_CLASSES.items():
            load_csv(key, value)
        print('Загрузка завершена!')


def load_csv(name_file, class_obj):
    with open(CSV_FILES_DIR + name_file + '.csv', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for row in csv_reader:
            valid_row = chek_keys(row)
            new_obj = class_obj(**valid_row)
            new_obj.save()
        print(
            f'Загружен файл [{name_file}], записей добавлено [{csv_reader.line_num-1}]')


def chek_keys(data_csv):
    data_csv_copy = data_csv.copy()
    for old_key in data_csv:
        if old_key in FIELDS:
            data_csv_copy[FIELDS[old_key]] = data_csv[old_key]
            del data_csv_copy[old_key]
    return data_csv_copy
