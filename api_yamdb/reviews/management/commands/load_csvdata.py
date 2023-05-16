import csv
import sqlite3

from django.core.management.base import BaseCommand
from django.conf import settings

TABLE_FILE = {
    'reviews_category': 'category.csv',
    'reviews_genre': 'genre.csv',
    'reviews_title': 'titles.csv',
    'reviews_title_genre': 'genre_title.csv',
    'reviews_comment': 'comments.csv',
    'reviews_review': 'review.csv',
    'reviews_user': 'users.csv',
}
USER_EXTRA_DATA = {
    "is_superuser": 0,
    'is_active': 0,
    "date_joined": "2023-05-06",
    "is_staff": 0,
}

CSV_DATA_PATH = settings.CSV_DATA_PATH
DB_PATH = settings.DATABASES['default']['NAME']


class Command(BaseCommand):

    def _connect_to_sqlite_db(self, db_path, sql_query, params=None):
        """Connect to sqlite db and perform sql query."""
        with sqlite3.connect(db_path) as con:
            cur = con.cursor()
            if params:
                cur.execute(sql_query, params)
            else:
                cur.execute(sql_query)

    def _delete_from_table(self, table_name):
        """Delete data from sqlite table"""
        sql_query = f'DELETE FROM {table_name};'
        self._connect_to_sqlite_db(DB_PATH, sql_query)
        print(f'Таблица {table_name} отчищена от старых данных')

    def _load_csv(self, table_name, file_path):
        """Load data from csv file into sqlite db."""
        with open(file_path, 'r', encoding='utf-8') as file:
            data = csv.reader(file, delimiter=',')
            first_row = next(data)
            if table_name == 'reviews_user':
                first_row += list(USER_EXTRA_DATA.keys())
            columns = ', '.join(first_row)
            placeholders = ', '.join(len(first_row) * '?')
            sql_query_update = (f'INSERT INTO {table_name}({columns}) '
                                f'VALUES({placeholders});')
            for row in data:
                if table_name == 'reviews_user':
                    row += list(USER_EXTRA_DATA.values())
                self._connect_to_sqlite_db(DB_PATH, sql_query_update, row)
            print(f'{table_name} загружена данными из файла {file_path}')

    def handle(self, *args, **options):
        for table, csv_file in TABLE_FILE.items():
            file_path = CSV_DATA_PATH / csv_file
            self._delete_from_table(table)
            self._load_csv(table, file_path)
            print('Загрузка окончена.')
