from django.core.management.base import BaseCommand

from deals.services.deals_sync import deactivate_old_deals


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--days", type=int, default=7, help="Kicked days")

    def handle(self, *args, **options):
        days = options["days"]
        count = deactivate_old_deals(days=days)
        self.stdout.write(self.style.SUCCESS(f"...{count}..."))
