import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import uuid

load_dotenv()
BASE_URL = os.getenv("BASE_URL")


# ----------------
# Helper Functions
# ----------------

class TestingFunctionsClass:
    @staticmethod
    def new_user_payload():
        unique_email = f"kamle_{uuid.uuid4()}@orm.com"
        username = f"kamel_{uuid.uuid4()}"
        return {
            "email": unique_email,
            "username": username,
            "password": "password"
        }

    @staticmethod
    def payload_for_generate_token():
        return {
            "username": "kamle@orm.com",
            "password": "password"
        }

    @staticmethod
    def updated_user_payload():
        return {
            "username": "tinyFrog12",
            "email": "kamle@orm.com",
            "password": "password"
        }

    @staticmethod
    def create_user(payload):
        response = requests.post(BASE_URL + "/users", json=payload)
        if response.status_code != 201:
            print("Failed to create user:", response.status_code, response.text)
        return response

    @staticmethod
    def update_user_with_id(user_id, payload):
        return requests.put(BASE_URL + f"/users/{user_id}", json=payload)

    @staticmethod
    def delete_user_with_id(user_id):
        return requests.delete(BASE_URL + f"/users/{user_id}")

    @staticmethod
    def get_user_with_id(user_id):
        return requests.get(BASE_URL + f"/users/{user_id}")

    @staticmethod
    def generate_token(payload):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        return requests.post(f"{BASE_URL}/token", data=payload, headers=headers)

    @staticmethod
    def get_current_user(token):
        headers = {"Authorization": f"Bearer {token}"}
        return requests.get(f"{BASE_URL}/users/me", headers=headers)

    @staticmethod
    def update_me(payload, token):
        headers = {"Authorization": f"Bearer {token}"}
        return requests.put(f"{BASE_URL}/users/me", json=payload, headers=headers)

    @staticmethod
    def delete_me(token):
        headers = {"Authorization": f"Bearer {token}"}
        return requests.delete(f"{BASE_URL}/users/me", headers=headers)

    @staticmethod
    def new_blog_payload():
        return {
            "title": "My First Blog",
            "content": "This is a test blog content."
        }

    @staticmethod
    def updated_blog_payload():
        return {
            "title": "Updated Blog Title",
            "content": "This is updated content.",
            "updated_at": datetime.utcnow().isoformat()
        }

    @staticmethod
    def create_blog(payload, token):
        headers = {"Authorization": f"Bearer {token}"}
        return requests.post(BASE_URL + "/blogs", json=payload, headers=headers)

    @staticmethod
    def get_blog_with_id(blog_id, token):
        headers = {"Authorization": f"Bearer {token}"}
        return requests.get(BASE_URL + f"/blogs/{blog_id}", headers=headers)

    @staticmethod
    def update_blog_with_id(blog_id, payload, token):
        headers = {"Authorization": f"Bearer {token}"}
        return requests.put(BASE_URL + f"/blogs/{blog_id}", json=payload, headers=headers)

    @staticmethod
    def delete_blog_with_id(blog_id, token):
        headers = {"Authorization": f"Bearer {token}"}
        return requests.delete(BASE_URL + f"/blogs/{blog_id}", headers=headers)

    @staticmethod
    def get_all_blogs(token):
        headers = {"Authorization": f"Bearer {token}"}
        return requests.get(BASE_URL + "/blogs", headers=headers)

