from fastapi.testclient import TestClient
from main import app


def execute_request(payload):
    client = TestClient(app)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    print("\n\n[TEST] Execute Request:\n")
    response = client.post("/api/calc-power", json=payload, headers=headers)
    print("\n[TEST] Response: " + response.text)

    return response

def test_calculate_full_model():
    payload = {
        "cpu_freq": 3000,
        "cpu_threads": 8,
        "cpu_cores": 4,
        "tdp": 65,
        "release_year": 2022,
        "ram": 16,
        "architecture": "haswell",
        "cpu_make": "intel"
    }

    response = execute_request(payload)

    assert response.status_code == 200
    assert "powerModel" in response.json()
    assert "sourceUrl" in response.json()
    assert "powerData" in response.json()

def test_calculate_half_model():
    payload = {
        "cpu_freq": 3000,
        "cpu_threads": 8,
        "cpu_cores": 4,
        "tdp": 65,
        "release_year": 2022,
        "ram": None,
        "architecture": None,
        "cpu_make": None
    }

    response = execute_request(payload)

    assert response.status_code == 200
    assert "powerModel" in response.json()
    assert "sourceUrl" in response.json()
    assert "powerData" in response.json()

def test_calculate_minimal_model():
    payload = {
        "cpu_freq": None,
        "cpu_threads": None,
        "cpu_cores": 4,
        "tdp": None,
        "release_year": None,
        "ram": None,
        "architecture": None,
        "cpu_make": None
    }

    response = execute_request(payload)

    assert response.status_code == 200
    assert "powerModel" in response.json()
    assert "sourceUrl" in response.json()
    assert "powerData" in response.json()

def test_calculate_empty_model():
    payload = {
        "cpu_freq": None,
        "cpu_threads": None,
        "cpu_cores": None,
        "tdp": None,
        "release_year": None,
        "ram": None,
        "architecture": None,
        "cpu_make": None
    }

    response = execute_request(payload)

    assert response.status_code == 200
    assert "powerModel" in response.json()
    assert "sourceUrl" in response.json()
    assert "powerData" in response.json()
