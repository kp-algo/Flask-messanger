import pytest
from unittest.mock import patch
from run import app 


# Fixtures: Setup the test environment
@pytest.fixture
def client():
    """Configures the Flask app for testing and yields a test client."""
    app.config['TESTING'] = True
    app.config['DEBUG'] = False
    
    with app.test_client() as client:
        yield client



#Health Check Test (Kubernetes Liveness Probe)
def test_health_check(client):
    """Verify that the health check endpoint returns 200 OK."""
    response = client.get('/health')
    
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


#Sending a Message (Valid Payload)
def test_send_message_success(client):
    """Test pushing a valid message payload."""
    payload = {
        "sender": "alice",
        "recipient": "bob",
        "message": "Hello, Bob!"
    }
    
    response = client.post(
        '/api/messages',
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    assert response.status_code in (200, 201)
    json_data = response.get_json()
    assert json_data["status"] == "success" or "id" in json_data

#Input Validation (Missing Required Fields)
def test_send_message_missing_field(client):
    """Ensure sending an incomplete payload yields a 400 Bad Request."""
    bad_payload = {
        "sender": "alice"
        # Missing 'recipient' and 'message'
    }
    
    response = client.post('/api/messages', json=bad_payload)
    
    assert response.status_code == 400


#Redis
@patch('app.redis_client')  # Replaces your real Redis client with a fake mock
def test_send_message_with_redis_mock(mock_redis, client):
    """Tests message publishing without needing a live Redis server running."""
    # Define what the fake Redis operation should return
    mock_redis.publish.return_value = 1
    
    payload = {
        "sender": "alice",
        "recipient": "bob",
        "message": "Mocked test message"
    }
    
    response = client.post('/api/messages', json=payload)
    assert response.status_code in (200, 201)