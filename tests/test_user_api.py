import requests
from tests.testing_functions import TestingFunctionsClass
from dotenv import load_dotenv
import os

load_dotenv()
BASE_URL = os.getenv("BASE_URL")

# def test_can_call_endpoint():
#     response = requests.get(BASE_URL + "/users")
#     assert response.status_code == 200


# def test_can_create_and_delete_and_update_user():
#     payload = TestingFunctionsClass.new_user_payload()
#     updated_payload = TestingFunctionsClass.updated_user_payload()
#     response = TestingFunctionsClass.create_user(payload)

#     assert response.status_code == 201
#     assert response.json()["email"] == payload["email"]

#     user_id = response.json()["id"]
#     response = TestingFunctionsClass.get_user_with_id(user_id)
#     assert response.status_code == 200

#     response = TestingFunctionsClass.update_user_with_id(
#         user_id, updated_payload)
#     assert response.json()["username"] == updated_payload["username"]

#     response = TestingFunctionsClass.delete_user_with_id(user_id)
#     assert response.status_code == 204

#     response = TestingFunctionsClass.get_user_with_id(user_id)
#     assert response.status_code == 404


# def test_can_create_user():
#     payload = TestingFunctionsClass.new_user_payload()
#     response = TestingFunctionsClass.create_user(payload)

#     assert response.status_code == 201
#     assert response.json()["email"] == payload["email"]


# def test_can_generate_token():
#     token_payload = TestingFunctionsClass.payload_for_generate_token()

#     response = TestingFunctionsClass.generate_token(token_payload)
#     assert response.status_code == 200


# def test_can_get_me():
#     token_payload = TestingFunctionsClass.payload_for_generate_token()

#     response = TestingFunctionsClass.generate_token(token_payload)
#     assert response.status_code == 200
#     token = response.json()["access_token"]

#     response = TestingFunctionsClass.get_current_user(token)
#     assert response.status_code == 200
#     assert response.json()["email"] == token_payload["username"]


# def test_can_update_me():
#     token_payload = TestingFunctionsClass.payload_for_generate_token()
#     updated_payload = TestingFunctionsClass.updated_user_payload()

#     response = TestingFunctionsClass.generate_token(token_payload)
#     assert response.status_code == 200
#     token = response.json()["access_token"]

#     response = TestingFunctionsClass.update_me(updated_payload, token)
#     assert response.status_code == 200
#     assert response.json()["email"] == updated_payload["email"]


# def test_can_delete_me():
#     token_payload = TestingFunctionsClass.payload_for_generate_token()

#     response = TestingFunctionsClass.generate_token(token_payload)
#     assert response.status_code == 200
#     token = response.json()["access_token"]

#     response = TestingFunctionsClass.delete_me(token)
#     assert response.status_code == 204

#     response = TestingFunctionsClass.get_current_user(token)
#     assert response.status_code == 404


# for running the server testing use
# ptw
# or
# py -m pytest -v -s

# venv\Scripts\activate; cd backend; uvicorn main:app --reload
