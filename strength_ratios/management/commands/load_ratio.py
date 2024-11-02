# ratios/management/commands/load_ratios.py

import csv
from django.core.management.base import BaseCommand
from strength_ratios.models import StrengthRatio

class Command(BaseCommand):
    help = 'Load strength ratios from a CSV file'

    def handle(self, *args, **kwargs):
        with open('strength_ratios.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                StrengthRatio.objects.create(
                    exercise=row['exercise'],
                    equipment_type=row['equipment_type'],
                    gender=row['gender'],
                    min_age=int(row['min_age']),
                    max_age=int(row['max_age']),
                    ratio=float(row['ratio'])
                )
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
