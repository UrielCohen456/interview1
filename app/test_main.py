from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_ip_from_header_equals_header():
    response = client.get("/", headers={"x-forwarded-for": "8.8.8.8, 10.10.10.10, 30.30.30.30"})
    assert response.status_code == 200
    assert response.text == "8.8.8.8"

def test_get_ip_from_header_not_equals_header():
    response = client.get("/", headers={"x-forwarded-for": "9.9.9.9, 10.10.10.10, 30.30.30.30"})
    assert response.status_code == 200
    assert response.text != "8.8.8.8"

def test_get_localhost_ip_returns_testclient():
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == "testclient"


