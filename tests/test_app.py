import pytest
from app import app
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_homepage(client):
    """Test the homepage."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Flask App is Running" in response.data  # Update to match actual content

