import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from urllib.parse import quote
from dodgerblue.settings import NODEHOSTNAME
from .models import Author


User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_author():
    def _create_author(username, password, display_name, state='ACTIVE', is_staff=False, is_local=True):
        user = User.objects.create_user(username=username, password=password, is_staff=is_staff)
        author = Author.objects.create(username=username,
                                       displayName=display_name,
                                       state=state,
                                       user=user,
                                       host=NODEHOSTNAME,
                                       is_local=is_local)
        author.id_url = f"{NODEHOSTNAME}/api/authors/{author.id}"
        author.page = f"{NODEHOSTNAME}/authors/{author.id}"
        author.save()
        return user, author
    return _create_author


@pytest.mark.django_db
def test_author_login_success(api_client, create_author):
    user, author = create_author("testuser", "securepassword", "Test User")
    author.state = "ACTIVE"
    author.save()
    response = api_client.post("/api/authors/login", {"username": "testuser", "password": "securepassword"})

    assert response.status_code == status.HTTP_200_OK
    assert "message" in response.data
    assert response.data["user"]["username"] == "testuser"

@pytest.mark.django_db
def test_author_login_invalid_credentials(api_client):
    response = api_client.post("/api/authors/login", {"username": "nonexistent", "password": "wrongpass"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "error" in response.data

@pytest.mark.django_db
def test_author_login_pending_account(api_client, create_author):
    user, author = create_author("inactiveuser", "securepassword", "Inactive User", state='PENDING')
    response = api_client.post("/api/authors/login", {"username": "inactiveuser", "password": "securepassword"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "error" in response.data

@pytest.mark.django_db
def test_author_signup_success(api_client):
    response = api_client.post("/api/authors/signup", {"username": "newuser", "password": "securepassword", "displayName": "New User"})

    assert response.status_code == status.HTTP_201_CREATED
    assert "message" in response.data
    assert response.data["user"]["username"] == "newuser"

@pytest.mark.django_db
def test_retrieve_collection_of_authors(api_client, create_author):
    [create_author(f"user{i}", "123", f"User {i}") for i in range(15)]
    response = api_client.get("/api/authors")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["type"] == "authors"
    assert "count" in response.data
    assert "next" in response.data
    assert "previous" in response.data
    assert "authors" in response.data
    assert len(response.data["authors"]) == 10

@pytest.mark.django_db
def test_author_signup_missing_fields(api_client):
    response = api_client.post("/api/authors/signup", {"username": "newuser"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "password" in response.data
    assert "displayName" in response.data

@pytest.mark.django_db
def test_get_author_by_id_url_not_found(api_client):
    encoded_url = quote("http://nonexistent.url")
    response = api_client.get(f"/api/authors/{encoded_url}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "error" in response.data

@pytest.mark.django_db
def test_get_current_user_authenticated(api_client, create_author):
    user, author = create_author("testuser", "securepassword", "Test User")
    api_client.force_authenticate(user=user)
    response = api_client.get(f"/api/authors/current-user")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["user"]["username"] == author.username

@pytest.mark.django_db
def test_get_current_user_unauthenticated(api_client):
    response = api_client.get("/api/authors/current-user")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "error" in response.data

@pytest.mark.django_db
def test_node_admin_changes_author_state(api_client, create_author):
    admin_user, admin_author = create_author("admin", "securepassword", "Admin User", is_staff=True)
    user, author = create_author("testuser", "securepassword", "Test User", state="PENDING")
    assert author.state == "PENDING"
    api_client.force_authenticate(user=admin_user)
    response = api_client.put(f"/api/authors/{author.id}", {"state": "ACTIVE"})

    assert response.status_code == status.HTTP_200_OK
    author.refresh_from_db()
    assert author.state == "ACTIVE"

@pytest.mark.django_db
def test_normal_user_cannot_change_author_state(api_client, create_author):
    user, author = create_author("testuser", "securepassword", "Test User", state="PENDING")
    user_2, author_2 = create_author("normaluser", "securepassword", "Normal User")
    api_client.force_authenticate(user=user_2)
    response = api_client.put(f"/api/authors/{author.id}", {"state": "DELETED"})

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert author.state == "PENDING"
