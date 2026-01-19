from decimal import Decimal

import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from deals.models import Store,Deal
@pytest.fixture
def api_client():
    return APIClient()




@pytest.fixture
def sample_deals(db):
    steam = baker.make(Store, name="Steam", external_id=1)
    gog = baker.make(Store, name="GOG", external_id=2)
    stores = steam,gog
    baker.make(
        Deal,
        store=steam,
        title="The Witcher 3",
        discount_percent=80,
        normal_price=Decimal("59.99"),
        sale_price=Decimal("11.99"),
        currency="EUR",
        is_active=True,
        external_id=1001,
        url="https://example.com/1001",
    )
    baker.make(
        Deal,
        store=gog,
        title="Hades",
        discount_percent=40,
        normal_price=Decimal("24.99"),
        sale_price=Decimal("14.99"),
        currency="EUR",
        is_active=True,
        external_id=1002,
        url="https://example.com/1002",
    )
    baker.make(
        Deal,
        store=steam,
        title="Portal 2",
        discount_percent=60,
        normal_price=Decimal("9.99"),
        sale_price=Decimal("3.99"),
        currency="EUR",
        is_active=True,
        external_id=1003,
        url="https://example.com/1003",
    )
    return stores