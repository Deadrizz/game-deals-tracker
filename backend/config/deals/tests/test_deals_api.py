import time
from datetime import timedelta
from decimal import Decimal
from deals.services.deals_sync import deactivate_old_deals,seed_demo_deals
import pytest
from deals.models import Deal

@pytest.mark.django_db
def test_api_deals(sample_deals, api_client):
    response = api_client.get("/api/deals/")
    data = response.json()
    assert response.status_code == 200
    assert "results" in data
    assert len(data["results"]) >= 1


@pytest.mark.django_db
def test_min_discount_deal(sample_deals, api_client):
    response = api_client.get("/api/deals/?min_discount=50")
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) >= 1
    for item in data["results"]:
        assert item["discount_percent"] >= 50


@pytest.mark.django_db
def test_max_price_deal(sample_deals, api_client):
    response = api_client.get("/api/deals/?max_price=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) >= 1
    for item in data["results"]:
        assert Decimal(item["sale_price"]) <= Decimal("10")


@pytest.mark.django_db
def test_search_title_deal(sample_deals, api_client):
    response = api_client.get("/api/deals/?search=witcher")
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) >= 1
    for item in data["results"]:
        title = item["title"].lower()
        assert "witcher" in title


@pytest.mark.django_db
def test_ordering_deal(sample_deals, api_client):
    response = api_client.get("/api/deals/?ordering=-discount_percent")
    assert response.status_code == 200
    data = response.json()
    discount = [item["discount_percent"] for item in data["results"]]
    assert discount[0] == 80
    for i in range(len(discount) - 1):
        assert discount[i] >= discount[i + 1]

@pytest.mark.django_db
def test_filter_by_store(sample_deals, api_client):
    steam, gog = sample_deals
    steam_id = steam.id
    response = api_client.get(f"/api/deals/?store={steam_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) >= 1
    store = [item["store"] for item in data["results"]]
    assert set(store) == {steam_id}

@pytest.mark.django_db
def test_deactivate_old_deals(sample_deals_for_days):
    deal_1,deal_2 = sample_deals_for_days
    result = deactivate_old_deals(7)
    deal_2.refresh_from_db()
    deal_1.refresh_from_db()
    assert result == 1
    assert deal_1.is_active == False
    assert deal_2.is_active == True

@pytest.mark.django_db
def test_seed_demo_deals():
    start_1 = seed_demo_deals()
    count_1 = Deal.objects.count()
    start_2 = seed_demo_deals()
    count_2 = Deal.objects.count()
    assert count_1 == count_2
    assert start_2 == 0

