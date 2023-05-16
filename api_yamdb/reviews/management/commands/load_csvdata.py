import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()
import csv
import sqlite3

from django.core.management.base import BaseCommand, CommandError
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
CSV_DATA_PATH = settings.CSV_DATA_PATH
DB_PATH = settings.DATABASES['default']['NAME']


class Command(BaseCommand):

    def _connect_to_sqlite_db(self, db_path, sql_query, params=None):
        with sqlite3.connect(db_path) as con:
            cur = con.cursor()
            if params:
                print(sql_query)
                cur.execute(sql_query, params)
            else:
                cur.execute(sql_query)

    def _delete_from_table(self, table_name):
        sql_query = f'DELETE FROM {table_name};'
        self._connect_to_sqlite_db(DB_PATH, sql_query)

    def _load_csv(self, table_name, file_path):  
        with open(file_path, 'r', encoding='utf-8') as file:
            data = csv.reader(file, delimiter=',')
            first_row = next(data)
            columns = ', '.join(first_row)
            placeholders = ', '.join(len(first_row) * '?')
            sql_query_update = (f'INSERT INTO {table_name}({columns}) '
                                f'VALUES({placeholders});')
            for row in data:
                self._connect_to_sqlite_db(DB_PATH, sql_query_update, row)

    def handle(self, *args, **options):
        for table, csv_file in TABLE_FILE.items():
            file_path = CSV_DATA_PATH / csv_file
            self._delete_from_table(table)
            self._load_csv(table, file_path)
