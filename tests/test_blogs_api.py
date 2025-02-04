from tests.testing_functions import TestingFunctionsClass
from dotenv import load_dotenv
import os

load_dotenv()
BASE_URL = os.getenv("BASE_URL")

def test_can_create_user():
    payload = TestingFunctionsClass.new_user_payload()
    response = TestingFunctionsClass.create_user(payload)
    assert response.status_code == 201
    assert response.json()["email"] == payload["email"]

def test_can_generate_token():
    token_payload = TestingFunctionsClass.payload_for_generate_token()
    response = TestingFunctionsClass.generate_token(token_payload)
    assert response.status_code == 200

def test_can_get_me():
    token_payload = TestingFunctionsClass.payload_for_generate_token()
    token_response = TestingFunctionsClass.generate_token(token_payload)
    assert token_response.status_code == 200
    token = token_response.json()["access_token"]
    response = TestingFunctionsClass.get_current_user(token)
    assert response.status_code == 200
    assert response.json()["email"] == token_payload["username"]

def test_can_update_me():
    token_payload = TestingFunctionsClass.payload_for_generate_token()
    updated_payload = TestingFunctionsClass.updated_user_payload()
    token_response = TestingFunctionsClass.generate_token(token_payload)
    assert token_response.status_code == 200
    token = token_response.json()["access_token"]
    response = TestingFunctionsClass.update_me(updated_payload, token)
    assert response.status_code == 200
    assert response.json()["email"] == updated_payload["email"]

def test_can_create_and_delete_and_update_blog():
    token_payload = TestingFunctionsClass.payload_for_generate_token()
    token_response = TestingFunctionsClass.generate_token(token_payload)
    assert token_response.status_code == 200
    token = token_response.json()["access_token"]

    payload = TestingFunctionsClass.new_blog_payload()
    updated_payload = TestingFunctionsClass.updated_blog_payload()    
    response = TestingFunctionsClass.create_blog(payload, token)      
    assert response.status_code == 201
    assert response.json()["title"] == payload["title"]

    blog_id = response.json()["id"]
    response = TestingFunctionsClass.get_blog_with_id(blog_id, token) 
    assert response.status_code == 200

    response = TestingFunctionsClass.update_blog_with_id(blog_id, updated_payload, token)
    data = response.json()
    assert "title" in data, f"Response JSON does not contain 'title': {data}"
    assert data["title"] == updated_payload["title"]

    response = TestingFunctionsClass.delete_blog_with_id(blog_id, token)
    assert response.status_code == 204

    response = TestingFunctionsClass.get_blog_with_id(blog_id, token)
    assert response.status_code == 404

def test_can_create_blog():
    token_payload = TestingFunctionsClass.payload_for_generate_token()
    token_response = TestingFunctionsClass.generate_token(token_payload)
    assert token_response.status_code == 200
    token = token_response.json()["access_token"]

    payload = TestingFunctionsClass.new_blog_payload()
    response = TestingFunctionsClass.create_blog(payload, token)
    assert response.status_code == 201
    assert response.json()["title"] == payload["title"]

def test_can_delete_me():
    token_payload = TestingFunctionsClass.payload_for_generate_token()
    token_response = TestingFunctionsClass.generate_token(token_payload)
    assert token_response.status_code == 200
    token = token_response.json()["access_token"]

    response = TestingFunctionsClass.delete_me(token)
    assert response.status_code == 204

    response = TestingFunctionsClass.get_current_user(token)
    assert response.status_code in (404, 500)
