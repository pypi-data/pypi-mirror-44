from django.core.cache import cache
from django.core.management.base import BaseCommand

from bi.lib import get_datasets_list


class Command(BaseCommand):
    help = 'Warms up cache'

    def handle(self, *args, **options):
        cache.clear()
        datasets = get_datasets_list()
        for dataset in datasets:
            dataset.get_dataframe()
        self.stdout.write(self.style.SUCCESS('Cache was successfully warmed up'))
