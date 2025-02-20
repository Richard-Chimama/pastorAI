import pytest
from flask import Flask
from uuid import UUID
from pg import app  # Replace `your_app_module` with the name of your Python file

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_new_user(client):
    """Test the /new-user endpoint."""
    # Send a GET request to the /new-user endpoint
    response = client.get('/new-user')

    # Check that the response status code is 200 (OK)
    assert response.status_code == 200

    # Parse the JSON response
    data = response.get_json()

    # Check that the response contains a "user_id" key
    assert 'user_id' in data

    # Check that the "user_id" is a valid UUID
    try:
        UUID(data['user_id'], version=4)
    except ValueError:
        pytest.fail("user_id is not a valid UUID")