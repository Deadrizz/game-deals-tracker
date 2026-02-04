from django.core.management.base import BaseCommand

from deals.services.notifications import noti_demo_telegram


class Command(BaseCommand):
    def handle(self, *args, **options):
        noti = noti_demo_telegram()
        self.stdout.write(self.style.SUCCESS(f"Your notifications:{noti}"))
