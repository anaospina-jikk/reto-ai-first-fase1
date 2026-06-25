import os
import time

import httpx
import pytest
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

_sku_counter = 0


def _unique_sku(prefix: str = "QA") -> str:
    global _sku_counter
    _sku_counter += 1
    return f"{prefix}-{int(time.time() * 1000)}-{_sku_counter:02d}"


def _product_payload(**overrides):
    data = {
        "name": "Producto QA",
        "sku": _unique_sku(),
        "cost_cents": 1000,
        "price_cents": 1500,
        "stock": 10,
        "min_stock": 2,
        "supplier_id": 1,
    }
    data.update(overrides)
    return data


def _movement_payload(product_id: int, type_: str = "OUT", qty: int = 1, **overrides):
    data = {"product_id": product_id, "type": type_, "qty": qty, "notes": "prueba QA"}
    data.update(overrides)
    return data


class TestHealth:
    def test_health_ok(self):
        resp = client.get("/api/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}


class TestSuppliers:
    def test_list_suppliers(self):
        resp = client.get("/api/suppliers")
        assert resp.status_code == 200
        body = resp.json()
        assert isinstance(body, list)
        assert len(body) >= 3


class TestProducts:
    def test_list_products(self):
        resp = client.get("/api/products")
        assert resp.status_code == 200
        body = resp.json()
        assert isinstance(body, list)
        assert len(body) >= 6

    def test_get_existing_product(self):
        resp = client.get("/api/products/1")
        assert resp.status_code == 200
        body = resp.json()
        assert body["id"] == 1
        assert "name" in body and "sku" in body

    def test_get_missing_product(self):
        resp = client.get("/api/products/9999")
        assert resp.status_code == 404

    def test_create_product_happy(self):
        payload = _product_payload(name="Impresora", sku=_unique_sku("IMP"))
        resp = client.post("/api/products", json=payload)
        assert resp.status_code == 201
        body = resp.json()
        assert body["name"] == payload["name"]
        assert body["sku"] == payload["sku"]

    def test_create_product_conflict_sku(self):
        sku = _unique_sku("CFL")
        first = client.post("/api/products", json=_product_payload(name="Uno", sku=sku))
        assert first.status_code == 201
        second = client.post(
            "/api/products", json=_product_payload(name="Dos", sku=sku)
        )
        assert second.status_code == 409

    def test_create_product_bad_supplier(self):
        payload = _product_payload(supplier_id=999)
        resp = client.post("/api/products", json=payload)
        assert resp.status_code == 400

    def test_create_product_negative_min_stock_is_accepted(self):
        payload = _product_payload(sku=_unique_sku("MIN"), min_stock=-1)
        resp = client.post("/api/products", json=payload)
        assert resp.status_code == 201
        body = resp.json()
        assert body["min_stock"] == -1

    def test_create_product_negative_cost_cents_is_accepted(self):
        payload = _product_payload(sku=_unique_sku("COST"), cost_cents=-1000)
        resp = client.post("/api/products", json=payload)
        assert resp.status_code == 201
        body = resp.json()
        assert body["cost_cents"] == -1000


class TestStockMovements:
    def setup_method(self):
        product = client.post("/api/products", json=_product_payload(sku=_unique_sku("MOV")))
        assert product.status_code == 201
        self.product = product.json()

    def test_register_in_movement(self):
        payload = _movement_payload(self.product["id"], type_="IN", qty=5)
        resp = client.post("/api/stock/movement", json=payload)
        assert resp.status_code == 201
        body = resp.json()
        assert body["type"] == "IN"
        assert body["qty"] == 5
        assert body["product_id"] == self.product["id"]

    def test_register_out_movement_decrements_stock(self):
        payload = _movement_payload(self.product["id"], type_="OUT", qty=2)
        resp = client.post("/api/stock/movement", json=payload)
        assert resp.status_code == 201
        product = client.get(f"/api/products/{self.product['id']}")
        assert product.json()["stock"] == 8

    def test_register_out_movement_negative_stock_accepted(self):
        payload = _movement_payload(self.product["id"], type_="OUT", qty=999)
        resp = client.post("/api/stock/movement", json=payload)
        assert resp.status_code == 201
        product = client.get(f"/api/products/{self.product['id']}")
        assert product.json()["stock"] < 0

    def test_register_movement_decimal_qty_accepted(self):
        payload = _movement_payload(self.product["id"], type_="IN", qty=2.5)
        resp = client.post("/api/stock/movement", json=payload)
        assert resp.status_code == 201
        body = resp.json()
        assert body["qty"] == 2.5


class TestStockAlerts:
    def test_alerts_happy(self):
        resp = client.get("/api/stock/alerts")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)


class TestAlertsFailMode:
    def setup_method(self):
        os.environ["ALERTS_FAIL"] = "1"
        app.dependency_overrides.clear()

    def teardown_method(self):
        os.environ.pop("ALERTS_FAIL", None)

    def test_alerts_endpoint_503(self):
        resp = client.get("/api/stock/alerts")
        assert resp.status_code == 503

    def test_out_movement_503_when_alerts_fail(self):
        product_resp = client.get("/api/products/1")
        product = product_resp.json()
        payload = _movement_payload(product["id"], type_="OUT", qty=1)
        resp = client.post("/api/stock/movement", json=payload)
        assert resp.status_code == 503
