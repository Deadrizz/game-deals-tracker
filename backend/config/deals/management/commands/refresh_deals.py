from django.core.management.base import BaseCommand

from deals.services.deals_sync import deactivate_old_deals, seed_demo_deals


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--days", type=int, default=7)

    def handle(self, *args, **options):
        days = options["days"]
        seed = seed_demo_deals()
        deactivated = deactivate_old_deals(days=days)
        self.stdout.write(
            self.style.SUCCESS(f"Created:{seed} deactivated:{deactivated}")
        )
