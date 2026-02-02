from deals.services.deals_sync import seed_demo_deals
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        created = seed_demo_deals()
        self.stdout.write(self.style.SUCCESS(f"...{created}..."))
