from django.core.management.base import BaseCommand

from metrics.models import Metric
from metrics.analysis import TextMetric

class Command(BaseCommand):
    help = 'Syncs predefined text metrics to the database'

    def handle(self, *args, **kwargs):
        for metric in TextMetric:
            metric_alias = metric.alias
            obj, created = Metric.objects.get_or_create(name=metric_alias)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Added metric {metric_alias}'))
            else:
                self.stdout.write(f'{metric_alias} already exists')