import pytest

from app import app, inventory


@pytest.fixture
def client():
    app.config["TESTING"] = True

    # Keep tests independent from one another.
    original_inventory = inventory.copy()

    with app.test_client() as client:
        yield client

    inventory.clear()
    inventory.extend(original_inventory)


def test_get_all_inventory(client):
    response = client.get("/inventory")

    assert response.status_code == 200
    data = response.get_json()

    assert "inventory" in data
    assert data["count"] >= 1


def test_get_single_item(client):
    response = client.get("/inventory/1")

    assert response.status_code == 200
    assert response.get_json()["id"] == 1


def test_get_missing_item(client):
    response = client.get("/inventory/9999")

    assert response.status_code == 404


def test_post_inventory(client):
    response = client.post(
        "/inventory",
        json={
            "product_name": "Test Juice",
            "price": 150,
            "stock": 10
        }
    )

    assert response.status_code == 201
    assert response.get_json()["product_name"] == "Test Juice"


def test_post_inventory_missing_fields(client):
    response = client.post(
        "/inventory",
        json={"product_name": "Incomplete Product"}
    )

    assert response.status_code == 400


def test_patch_inventory(client):
    response = client.patch(
        "/inventory/1",
        json={"price": 400, "stock": 25}
    )

    assert response.status_code == 200
    data = response.get_json()

    assert data["price"] == 400
    assert data["stock"] == 25


def test_delete_inventory(client):
    response = client.delete("/inventory/1")

    assert response.status_code == 200
    assert response.get_json()["item"]["id"] == 1

    response = client.get("/inventory/1")
    assert response.status_code == 404


def test_external_product_requires_search_value(client):
    response = client.get("/external-product")

    assert response.status_code == 400
