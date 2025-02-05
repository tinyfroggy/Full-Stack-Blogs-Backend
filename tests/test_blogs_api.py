from tests.testing_functions import TestingFunctionsClass
from dotenv import load_dotenv
import os
import pytest

load_dotenv()
BASE_URL = os.getenv("BASE_URL")

# ----------
# Fixtures
# ----------


@pytest.fixture
def test_user():
    """Fixture to create a fresh user for each test and return credentials"""
    user_payload = TestingFunctionsClass.new_user_payload()
    create_response = TestingFunctionsClass.create_user(user_payload)
    assert create_response.status_code == 201, "User setup failed"

    token_response = TestingFunctionsClass.generate_token(
        {"username": user_payload["email"], "password": user_payload["password"]}
    )
    assert token_response.status_code == 200, "Token setup failed"

    return {
        "payload": user_payload,
        "token": token_response.json()["access_token"],
        "id": create_response.json()["id"],
    }


@pytest.fixture
def test_blog(test_user):
    """Fixture to create a blog post for tests requiring existing content"""
    blog_payload = TestingFunctionsClass.new_blog_payload()
    create_response = TestingFunctionsClass.create_blog(
        blog_payload, test_user["token"]
    )
    assert create_response.status_code == 201, "Blog setup failed"

    return {
        "payload": blog_payload,
        "id": create_response.json()["id"],
        "token": test_user["token"],
    }


# ----------
# User Tests
# ----------


def test_user_lifecycle():
    """Test full user lifecycle: create, update, delete"""
    # Create user
    user_payload = TestingFunctionsClass.new_user_payload()
    create_response = TestingFunctionsClass.create_user(user_payload)
    assert create_response.status_code == 201
    user_id = create_response.json()["id"]

    # Test login
    token_response = TestingFunctionsClass.generate_token(
        {"username": user_payload["email"], "password": user_payload["password"]}
    )
    assert token_response.status_code == 200
    token = token_response.json()["access_token"]

    # Update user
    updated_payload = TestingFunctionsClass.updated_user_payload()
    update_response = TestingFunctionsClass.update_me(updated_payload, token)
    assert update_response.status_code == 200
    assert update_response.json()["username"] == updated_payload["username"]

    # Delete user
    delete_response = TestingFunctionsClass.delete_me(token)
    assert delete_response.status_code == 204

    # Verify deletion
    get_response = TestingFunctionsClass.get_user_with_id(user_id)
    assert get_response.status_code == 404


def test_authentication_flow(test_user):
    """Test authentication-related functionality"""
    # Test valid token usage
    me_response = TestingFunctionsClass.get_current_user(test_user["token"])
    assert me_response.status_code == 200
    assert me_response.json()["email"] == test_user["payload"]["email"]

    # Test invalid token
    invalid_token_response = TestingFunctionsClass.get_current_user("invalid_token")
    assert invalid_token_response.status_code in (401, 403)

    # delete user
    delete_response = TestingFunctionsClass.delete_me(test_user["token"])
    assert delete_response.status_code == 204

    # verify deletion
    get_response = TestingFunctionsClass.get_user_with_id(test_user["id"])
    assert get_response.status_code == 404


# ----------
# Blog Tests
# ----------


def test_create_blog(test_user):
    """Test creating and retrieving a blog post"""
    blog_payload = TestingFunctionsClass.new_blog_payload()
    create_response = TestingFunctionsClass.create_blog(
        blog_payload, test_user["token"]
    )
    assert create_response.status_code == 201, "Failed to create blog"
    blog_id = create_response.json()["id"]

    # Retrieve the newly created blog post
    get_response = TestingFunctionsClass.get_blog_with_id(blog_id, test_user["token"])
    assert get_response.status_code == 200, "Failed to retrieve blog"
    blog_data = get_response.json()
    assert blog_data["title"] == blog_payload["title"]
    assert blog_data["content"] == blog_payload["content"]



def test_update_blog(test_blog):
    """Test updating an existing blog post"""
    updated_payload = TestingFunctionsClass.updated_blog_payload()
    update_response = TestingFunctionsClass.update_blog_with_id(
        test_blog["id"], updated_payload, test_blog["token"]
    )
    assert update_response.status_code == 200, "Failed to update blog"
    updated_blog = update_response.json()
    assert updated_blog["title"] == updated_payload["title"]
    assert updated_blog["content"] == updated_payload["content"]


def test_delete_blog(test_blog):
    """Test deleting a blog post"""
    delete_response = TestingFunctionsClass.delete_blog_with_id(
        test_blog["id"], test_blog["token"]
    )
    assert delete_response.status_code == 204, "Failed to delete blog"

    # Verify deletion by attempting to retrieve the deleted blog
    get_response = TestingFunctionsClass.get_blog_with_id(
        test_blog["id"], test_blog["token"]
    )
    assert get_response.status_code == 404, "Blog was not deleted"


def test_get_all_blogs(test_user, test_blog):
    """Test retrieving all blog posts and verifying the created blog is in the list"""
    get_all_response = TestingFunctionsClass.get_all_blogs(test_user["token"])
    assert get_all_response.status_code == 200, "Failed to retrieve all blogs"
    blogs = get_all_response.json()

    # Check that the blog from the fixture is in the retrieved list
    blog_ids = [blog["id"] for blog in blogs]
    assert test_blog["id"] in blog_ids, "Created blog not found in all blogs"
