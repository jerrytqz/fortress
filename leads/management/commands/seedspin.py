from django.core.management.base import BaseCommand

from pathlib import Path
import csv
from leads.models import Item

BASE_PATH = Path(__file__).parent 
CSV_PATH = (BASE_PATH / '../../items.csv').resolve()

class Command(BaseCommand):
    help = 'Seeds the Spin database with items'

    def handle(self, *args, **kwargs):
        with open(CSV_PATH, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            
            # Skip header
            next(reader)

            for i, row in enumerate(reader):
                try:
                    item, created = Item.objects.update_or_create(
                        name=row[0],
                        defaults={'name': row[0], 'rarity': row[1], 'description': row[2]}
                    )
                
                    if created:
                        item.rarity = row[1]
                        item.description = row[2]
                        item.in_circulation = 0
                        item.save()
                except Exception as e:
                    print("Failed in row {} with {}".format(i + 2, e)) # Define header as row 1
                    break
