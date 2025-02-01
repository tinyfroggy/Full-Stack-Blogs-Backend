import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

import pytest
from print_color import print
import requests

BASE_URL = "/api/1"

@pytest.fixture(scope="module")
def test_user():
    payload = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass",
    }
    response = requests.post(f"{BASE_URL}/users", json=payload)
    
    assert response.status_code == 201, "❌ Failed to create user"
    
    user_data = response.json()
    yield user_data  # Return the test user data for use in other tests

    # Delete the test user
    requests.delete(f"{BASE_URL}/users/{user_data['id']}")

def create_user(email, username, password):
    payload = {"email": email, "username": username, "password": password}
    response = requests.post(f"{BASE_URL}/users", json=payload)
    return response

@pytest.mark.parametrize(
    "email, username, password, expected_status",
    [
        ("valid@email.com", "validuser", "strongpass", 201),  
        # ("invalidemail", "user1", "pass", 422),  
        # ("test@email.com", "", "pass", 422),  
    ],
)
def test_user_creation(email, username, password, expected_status):
    response = create_user(email, username, password)
    assert response.status_code == expected_status, (
        f"❌ Expected {expected_status}, got {response.status_code}"
    )

def test_create_user():
    payload = {
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "securepass",
    }
    response = requests.post(f"{BASE_URL}/users", json=payload)

    assert response.status_code == 201, "❌ Failed to create user"
    data = response.json()
    assert "id" in data
    assert data["email"] == payload["email"]

    print("✅ Response JSON: ", data, tag="success", tag_color="magenta", color="green")

def test_get_all_users():
    response = requests.get(f"{BASE_URL}/users")

    assert response.status_code == 200, f"❌ Status Code: {response.status_code}"
    print("✅ The Status Code is:", response.status_code, tag="success", tag_color="magenta", color="green")

# for running the server testing use 
# ptw
# or
# py -m pytest -v -s