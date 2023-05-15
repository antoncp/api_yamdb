import csv
import sqlite3
import os

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.apps import apps


TABLE_FILE = {
    'reviews_category': 'data/category.csv',
    'reviews_genre': 'data/genre.csv',
    'reviews_title': 'data/titles.csv',
    'reviews_title_genre': 'data/genre_title.csv',
    'reviews_comment': 'data/comments.csv',
    'reviews_review': 'data/review.csv',
    #'reviews_user': 'data/users.csv'
}
DB_PATH = settings.DATABASES['default']['NAME']


class Command(BaseCommand):

    def _connect_to_sqlite_database(self, db_path, sqlite_query, params=None):
        with sqlite3.connect(db_path) as con:
            cur = con.cursor()
            if params:
                cur.execute(sqlite_query, params)
            else:
                cur.execute(sqlite_query)

    def _load_csv(self, table_name, file):
        sql_query1 = f'DELETE FROM {table_name}'
        self._connect_to_sqlite_database(table_name, sql_query1)
        with open(file, 'r', encoding='utf-8') as file:
            data = csv.reader(file, delimiter=',')
            first_row = next(data)
            columns = ", ".join(first_row)
            placeholders = ', '.join(len(first_row) * '?')
            sql_query2 = f'INSERT INTO {table_name}({columns}) VALUES({placeholders});'
            for row in data:
                self._connect_to_sqlite_database(DB_PATH, sql_query2, row)

    def handle(self, *args, **options):
        for table, file in TABLE_FILE.items():
            self._load_csv(table, file)
