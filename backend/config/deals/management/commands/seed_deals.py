import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from deals.models import Deal, Store


class Command(BaseCommand):
    help = "Seed database with demo stores and deals"

    def handle(self, *args, **options):
        steam, _ = Store.objects.get_or_create(
            external_id=1, defaults={"name": "Steam"}
        )
        gog, _ = Store.objects.get_or_create(external_id=2, defaults={"name": "GOG"})

        stores = [steam, gog]
        titles = [
            "The Witcher 3",
            "Cyberpunk 2077",
            "Baldur's Gate 3",
            "Hades",
            "Disco Elysium",
            "Stardew Valley",
            "DOOM Eternal",
            "Red Dead Redemption 2",
            "Portal 2",
            "Hollow Knight",
        ]

        created = 0
        for i, title in enumerate(titles, start=1):
            store = random.choice(stores)
            normal = Decimal(random.choice(["19.99", "29.99", "39.99", "59.99"]))
            discount = random.choice([10, 20, 30, 40, 50, 60, 70, 80])
            sale = (
                normal * (Decimal("100") - Decimal(discount)) / Decimal("100")
            ).quantize(Decimal("0.01"))

            deal, was_created = Deal.objects.update_or_create(
                external_id=1000 + i,
                defaults={
                    "title": title,
                    "store": store,
                    "normal_price": normal,
                    "sale_price": sale,
                    "currency": "EUR",
                    "discount_percent": discount,
                    "url": f"https://example.com/deals/{1000 + i}",
                    "is_active": True,
                    "last_seen_at": timezone.now(),
                },
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Seed done. Created {created} deals."))
