import csv

from django.core.management.base import BaseCommand
from django.apps import apps
from django.conf import settings

MODEL_FILE = {
    'apps': {
        "users": {'User': 'users.csv'},
        "reviews": {
            'Category': 'category.csv',
            'Genre': 'genre.csv',
            'Title': 'titles.csv',
            'Title_genre': 'genre_title.csv',
            'Review': 'review.csv',
            'Comment': 'comments.csv'
        }
    }
}

CSV_DATA_PATH = settings.CSV_DATA_PATH


class Command(BaseCommand):
    help = 'Prepolutes db from csv files.'

    def _load_csv(self, file_path, model):
        """Load data from a csv file into a db table."""
        with open(file_path, 'r', encoding='utf-8') as file:
            data = csv.DictReader(file, delimiter=',')
            self.stdout.write(f'Loading {model}')
            for row in data:
                try:
                    model_instance = model(**row)
                    model_instance.save()
                except Exception as er:
                    self.stdout.write(f'{row} - {er}', ending='\n\n')
            self.stdout.write(f'{model} loading  is complete', ending='\n\n')

    def handle(self, *args, **options):
        for app_name, data in MODEL_FILE['apps'].items():
            for model_name, csv_file in data.items():
                model = apps.get_model(app_name, model_name)
                file_path = CSV_DATA_PATH / csv_file
                self._load_csv(file_path, model)
        self.stdout.write('The db prepopulation is complete.')
