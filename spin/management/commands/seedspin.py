from django.core.management.base import BaseCommand
from spin.models import Item

import csv
import urllib.request

CSV_PATH = 'https://starship.jerrytq.com/spin/items/items.csv'


class Command(BaseCommand):
    help = 'Seeds the Spin database with items'

    def handle(self, *args, **kwargs):
        try:
            response = urllib.request.urlopen(CSV_PATH)
            file = [l.decode('utf-8') for l in response.readlines()]
        except Exception as e:
            print("Could not open seeder file")
            return

        reader = csv.reader(file)
        next(reader)  # Skip header

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
                print("Failed in row {} with {}".format(i + 2, e))  # Define header as row 1
                break
