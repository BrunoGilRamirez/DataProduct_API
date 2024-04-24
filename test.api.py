from fastapi.testclient import TestClient
from main_dev import wdm, list_endpoints

client = TestClient(wdm)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == list_endpoints

def test_read_products():
    response = client.get("/products")
    assert response.status_code == 200

def test_read_product_by_id():
    response = client.get("/product_by_id/2674530000")
    assert response.status_code == 200

def test_read_product_by_id_not_found():
    response = client.get("/product_by_id/2674530001")
    assert response.status_code == 404

def test_read_product_by_id_invalid():
    response = client.get("/product_by_id/2674530000a")
    assert response.status_code == 422
              
