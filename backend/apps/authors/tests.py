import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from urllib.parse import quote
from dodgerblue.settings import NODEHOSTNAME
from .models import Author
import base64

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


@pytest.mark.django_db
def test_remote_author_creation(api_client, create_author):
    # node which sends the req
    node_user, node_author = create_author("nodeuser", "nodepassword", "Node User", state="ACTIVE")
    node_author.is_node = True
    node_author.save()

    # create the inbox owner
    _, local_author = create_author("localuser", "localpassword", "Local User", state="ACTIVE")

    remote_author_payload = {
        "id": "http://remote.host/api/authors/123",
        "host": "http://remote.host/api/",
        "displayName": "Remote Author",
        "profileImage": "http://remote.host/images/remote.png",
        "page": "http://remote.host/authors/123",
        "type": "author"
    }

    credentials = base64.b64encode("nodeuser:nodepassword".encode("utf-8")).decode("utf-8")
    api_client.credentials(HTTP_AUTHORIZATION=f"Basic {credentials}")

    url = f"/api/authors/{local_author.id}/inbox"
    response = api_client.post(url, remote_author_payload, format='json')

    assert response.status_code == status.HTTP_200_OK
    remote_author = Author.objects.get(id_url=remote_author_payload["id"])
    assert remote_author.displayName == "Remote Author"
    assert remote_author.is_local is False
    assert remote_author.state == "ACTIVE"


@pytest.mark.django_db
def test_remote_author_update(api_client, create_author):
    node_user, node_author = create_author("nodeuser2", "nodepassword", "Node User 2", state="ACTIVE")
    node_author.is_node = True
    node_author.save()

    _, local_author = create_author("localuser2", "localpassword", "Local User 2", state="ACTIVE")

    #create the remote author
    remote_author_payload = {
        "id": "http://remote.host/api/authors/456",
        "host": "http://remote.host/api/",
        "displayName": "Remote Author Original",
        "profileImage": "http://remote.host/images/original.png",
        "page": "http://remote.host/authors/456",
        "type": "author"
    }

    credentials = base64.b64encode("nodeuser2:nodepassword".encode("utf-8")).decode("utf-8")
    api_client.credentials(HTTP_AUTHORIZATION=f"Basic {credentials}")
    url = f"/api/authors/{local_author.id}/inbox"
    response = api_client.post(url, remote_author_payload, format='json')
    assert response.status_code == status.HTTP_200_OK
    remote_author = Author.objects.get(id_url=remote_author_payload["id"])
    assert remote_author.displayName == "Remote Author Original"

    # update the payload
    updated_payload = remote_author_payload.copy()
    updated_payload["displayName"] = "Remote Author Updated"

    response_update = api_client.post(url, updated_payload, format='json')
    assert response_update.status_code == status.HTTP_200_OK
    remote_author.refresh_from_db()
    assert remote_author.displayName == "Remote Author Updated"


@pytest.mark.django_db
def test_remote_author_missing_id(api_client, create_author):
    node_user, node_author = create_author("nodeuser3", "nodepassword", "Node User 3", state="ACTIVE")
    node_author.is_node = True
    node_author.save()

    _, local_author = create_author("localuser3", "localpassword", "Local User 3", state="ACTIVE")
    #missing id
    incomplete_payload = {
        # "id": "http://remote.host/api/authors/789",
        "host": "http://remote.host/api/",
        "displayName": "Incomplete Remote Author",
        "profileImage": "http://remote.host/images/incomplete.png",
        "page": "http://remote.host/authors/789",
        "type": "author"
    }

    credentials = base64.b64encode("nodeuser3:nodepassword".encode("utf-8")).decode("utf-8")
    api_client.credentials(HTTP_AUTHORIZATION=f"Basic {credentials}")
    url = f"/api/authors/{local_author.id}/inbox"
    response = api_client.post(url, incomplete_payload, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "id" in response.data


@pytest.mark.django_db
def test_discover_remote_author_unauthenticated(api_client):
    response = api_client.get("/api/authors/discover")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_discover_remote_author_authenticated(api_client, create_author, monkeypatch):
    """
    this is to test that an authenticated user can retrieve remote authors
    get_remote_authors helper is monkeypatched to return dummy data
    """

    user, local_author = create_author("localuser4", "localpassword", "Local User 4", state="ACTIVE")

    node_user, node_author = create_author("nodeuser4", "nodepassword", "Node User 4", state="ACTIVE")
    node_author.is_node = True
    node_author.host = "http://dummy.remote/api/"
    node_author.save()

    dummy_remote_data = {
        "authors": [
            {
                "id": "http://remote.node/api/authors/999",
                "host": "http://remote.node/api/",
                "displayName": "Remote Node Author",
                "profileImage": "http://remote.node/images/999.png",
                "page": "http://remote.node/authors/999",
                "type": "author"
            }
        ]
    }
    # patch the get_remote_authors function.
    # replace 'your_app.views' with the actual module path where get_remote_authors is imported.
    monkeypatch.setattr("apps.authors.views.get_remote_authors", lambda endpoint: dummy_remote_data)

    api_client.force_authenticate(user=user)
    response = api_client.get("/api/authors/discover")
    assert response.status_code == status.HTTP_200_OK
    data = response.data
    assert "authors" in data

    assert any(author["id"] == "http://remote.node/api/authors/999" for author in data["authors"])