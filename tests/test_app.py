import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Check that the index page loads correctly"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Snake" in response.data
