import pytest
from main import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_api_no_city(client):
    """Test when no city is provided."""
    response = client.post('/api', json={})
    assert response.status_code == 400
    assert b"City name is required" in response.data

def test_api_city_not_found(client, monkeypatch):
    """Test when city is not found and suggestions are returned."""

    class MockResponse:
        def __init__(self, status_code, json_data):
            self.status_code = status_code
            self._json = json_data
        def json(self):
            return self._json
        def raise_for_status(self):
            if self.status_code != 200:
                raise Exception("Not Found")

    def mock_get(url, *args, **kwargs):
        if "forecast" in url:
            return MockResponse(404, {})
        if "find" in url:
            return MockResponse(200, {"list": [{"name": "London"}, {"name": "Paris"}]})
        return MockResponse(200, {})

    monkeypatch.setattr("requests.get", mock_get)
    response = client.post('/api', json={"city": "FakeCity"})
    assert response.status_code == 404
    assert b"not found" in response.data
    assert b"London" in response.data
    assert b"Paris" in response.data

def test_api_success(client, monkeypatch):
    """Test a successful weather response with rain and high temperature."""

    class MockResponse:
        def __init__(self, status_code, json_data):
            self.status_code = status_code
            self._json = json_data
        def json(self):
            return self._json
        def raise_for_status(self):
            if self.status_code != 200:
                raise Exception("Not Found")

    # Mock forecast data with rain and high temperature
    mock_forecast = {
        "list": [
            {
                "dt_txt": "2024-06-01 12:00:00",
                "main": {"temp_max": 42, "temp_min": 30},
                "weather": [{"main": "Rain"}]
            },
            {
                "dt_txt": "2024-06-01 15:00:00",
                "main": {"temp_max": 41, "temp_min": 29},
                "weather": [{"main": "Clear"}]
            }
        ]
    }

    def mock_get(url, *args, **kwargs):
        if "forecast" in url:
            return MockResponse(200, mock_forecast)
        return MockResponse(200, {})

    monkeypatch.setattr("requests.get", mock_get)
    response = client.post('/api', json={"city": "Delhi"})
    assert response.status_code == 200
    data = response.get_json()
    # Check for rain and high temperature advice
    day = list(data.keys())[0]
    conditions = data[day]["conditions"]
    assert "Rain is expected, Please carry Umbrella" in conditions
    assert "Temerature is more than 40, Use sunscreen lotion" in conditions