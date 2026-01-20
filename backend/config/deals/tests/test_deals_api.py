from decimal import Decimal

import pytest


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


def test_filter_by_store(sample_deals, api_client):
    steam, gog = sample_deals
    steam_id = steam.id
    response = api_client.get(f"/api/deals/?store={steam_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) >= 1
    store = [item["store"] for item in data["results"]]
    assert set(store) == {steam_id}
