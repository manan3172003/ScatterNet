from django.test import TestCase

# Create your tests here.
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from dodgerblue.settings import NODEHOSTNAME
from ..authors.models import Author
from .models import Follow

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_author():
    def _create_author(username, password, display_name, state='ACTIVE', is_staff=False):
        user = User.objects.create_user(username=username, password=password, is_staff=is_staff)
        author = Author.objects.create(username=username, displayName=display_name, state=state, user=user, host=NODEHOSTNAME)
        author.id_url = f"http://localhost:8000/api/authors/{author.id}"
        author.save()

        return user, author

    return _create_author

@pytest.mark.django_db
def test_get_followers_no_followers(api_client, create_author):
    user, author = create_author("alice", "password", "Alice")
    url = f"/api/authors/{author.id}/followers"  # e.g. /api/authors/1/followers

    # List of followers shouldn't contain anything
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["type"] == "followers"
    assert isinstance(data["followers"], list)
    assert len(data["followers"]) == 0

@pytest.mark.django_db
def test_get_followers_with_one_follower(api_client, create_author):
    user_alice, author_alice = create_author("alice", "password", "Alice")
    user_bob, author_bob = create_author("bob", "password", "Bob")

    # Bob follows Alice (accepted follow)
    Follow.objects.create(actor=author_bob, object=author_alice, isPending=False)

    # Make a call to the list of followers without any query params (defaults to isPending=false)
    url = f"/api/authors/{author_alice.id}/followers"
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    # Should return a list of accepted followers, including Bob
    data = response.json()
    assert data["type"] == "followers"
    assert len(data["followers"]) == 1
    assert data["followers"][0]["id"] == author_bob.id_url
    assert data["followers"][0]["displayName"] == "Bob"

@pytest.mark.django_db
def test_get_followers_pending(api_client, create_author):
    user_alice, author_alice = create_author("alice", "password", "Alice")
    user_bob, author_bob = create_author("bob", "password", "Bob")

    # Bob has sent a follow request to Alice (pending)
    Follow.objects.create(actor=author_bob, object=author_alice, isPending=True)

    # Using the query param ?isPending=true
    url = f"/api/authors/{author_alice.id}/followers?isPending=true"
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    # Should return all pending follow requests, including Bob
    data = response.json()
    assert len(data["followers"]) == 1
    assert data["followers"][0]["displayName"] == "Bob"

@pytest.mark.django_db
def test_get_follower_detail_is_follower(api_client, create_author):
    user_alice, author_alice = create_author("alice", "password", "Alice")
    user_bob, author_bob = create_author("bob", "password", "Bob")

    # Bob is an accepted follower of Alice
    Follow.objects.create(actor=author_bob, object=author_alice, isPending=False)

    # Make a call that checks if Bob is a follower of Alice
    url = f"/api/authors/{author_alice.id}/followers/{author_bob.id_url}"

    # Should return author details of Bob
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == author_bob.id_url
    assert data["displayName"] == "Bob"

@pytest.mark.django_db
def test_get_follower_detail_not_follower(api_client, create_author):
    user_alice, author_alice = create_author("alice", "password", "Alice")
    user_bob, author_bob = create_author("bob", "password", "Bob")

    # No Follow object for Bob -> Alice
    url = f"/api/authors/{author_alice.id}/followers/{author_bob.id_url}"

    # Should state that Bob is not a follower
    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["error"] == "Not a follower"

@pytest.mark.django_db
def test_put_create_follow_request(api_client, create_author):
    user_alice, author_alice = create_author("alice", "password", "Alice")
    user_bob, author_bob = create_author("bob", "password", "Bob")

    # Bob logs in
    api_client.force_authenticate(user=user_bob)

    # Should say that a follow request was successfully created
    url = f"/api/authors/{author_alice.id}/followers/{author_bob.id_url}"
    response = api_client.put(url)
    assert response.status_code == status.HTTP_201_CREATED
    assert "Follow request successfully created" in response.json()["message"]

    # isPending should be true in DB
    follow_obj = Follow.objects.get(actor=author_bob, object=author_alice)
    assert follow_obj.isPending is True

@pytest.mark.django_db
def test_put_accept_follow_request(api_client, create_author):
    user_alice, author_alice = create_author("alice", "password", "Alice")
    user_bob, author_bob = create_author("bob", "password", "Bob")

    # Create a pending follow request from Bob->Alice
    follow_obj = Follow.objects.create(actor=author_bob, object=author_alice, isPending=True)

    # Alice logs in
    api_client.force_authenticate(user=user_alice)

    # Should say accepted
    url = f"/api/authors/{author_alice.id}/followers/{author_bob.id_url}"
    response = api_client.put(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Follow request accepted"

    # isPending should be false
    follow_obj.refresh_from_db()
    assert follow_obj.isPending is False

@pytest.mark.django_db
def test_delete_reject_follow_request(api_client, create_author):
    user_alice, author_alice = create_author("alice", "password", "Alice")
    user_bob, author_bob = create_author("bob", "password", "Bob")

    # Bob->Alice is pending
    follow_obj = Follow.objects.create(actor=author_bob, object=author_alice, isPending=True)

    # Alice logs in to reject
    api_client.force_authenticate(user=user_alice)

    # Should say request rejected
    url = f"/api/authors/{author_alice.id}/followers/{author_bob.id_url}"
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Follow request rejected"
    assert not Follow.objects.filter(pk=follow_obj.pk).exists()

@pytest.mark.django_db
def test_delete_unfollow(api_client, create_author):
    user_alice, author_alice = create_author("alice", "password", "Alice")
    user_bob, author_bob = create_author("bob", "password", "Bob")

    # Bob->Alice is accepted
    follow_obj = Follow.objects.create(actor=author_bob, object=author_alice, isPending=False)

    # Bob logs in to unfollow
    api_client.force_authenticate(user=user_bob)

    # Should say unfollowed successfully
    url = f"/api/authors/{author_alice.id}/followers/{author_bob.id_url}"
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Unfollowed successfully"
    assert not Follow.objects.filter(pk=follow_obj.pk).exists()

@pytest.mark.django_db
def test_get_following_list(api_client, create_author):
    user_alice, author_alice = create_author("alice", "password", "Alice")
    user_bob, author_bob = create_author("bob", "password", "Bob")

    # Alice follows Bob
    Follow.objects.create(actor=author_alice, object=author_bob, isPending=False)

    # Log in as alice
    api_client.force_authenticate(user=user_alice)

    # Make a call to Alice's following
    url = f"/api/authors/{author_alice.id}/following"
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    # Should include Bob
    data = response.json()
    assert data["type"] == "following"
    assert len(data["following"]) == 1
    assert data["following"][0]["id"] == author_bob.id_url

@pytest.mark.django_db
def test_get_friends_list(api_client, create_author):
    user_alice, author_alice = create_author("alice", "password", "Alice")
    user_bob, author_bob = create_author("bob", "password", "Bob")

    # Mutual follow: Bob->Alice, Alice->Bob
    Follow.objects.create(actor=author_bob, object=author_alice, isPending=False)
    Follow.objects.create(actor=author_alice, object=author_bob, isPending=False)

    api_client.force_authenticate(user=user_alice)

    # Should return a list of friends, which includes Bob
    url = f"/api/authors/{author_alice.id}/friends"
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["type"] == "following"
    assert len(data["friends"]) == 1
    assert data["friends"][0]["id"] == author_bob.id_url

@pytest.mark.django_db
def test_get_friend_detail(api_client, create_author):
    user_alice, author_alice = create_author("alice", "password", "Alice")
    user_bob, author_bob = create_author("bob", "password", "Bob")

    # Mutual follow
    Follow.objects.create(actor=author_bob, object=author_alice, isPending=False)
    Follow.objects.create(actor=author_alice, object=author_bob, isPending=False)

    # login as Alice
    api_client.force_authenticate(user=user_alice)

    # Should return the author in the response (Alice)
    url = f"/api/authors/{author_alice.id}/friends/{author_bob.id_url}"
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == author_alice.id_url