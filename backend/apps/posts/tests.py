from django.test import TestCase

# Create your tests here.

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from ..authors.models import Author
from .models import Post, Comment, Like

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_author():
    def _create_author(username, password, display_name, state='ACTIVE', is_staff=False):
        user = User.objects.create_user(username=username, password=password, is_staff=is_staff)
        author = Author.objects.create(username=username, displayName=display_name, state=state, user=user)
        author.id_url = f"http://localhost:8000/api/authors/{author.id}"
        author.save()

        return user, author

    return _create_author


@pytest.fixture
def create_post():
    def _create_post(author, title="Test Post", description="A test post", contentType="text/plain",
                     content="Hello", visibility="PUBLIC"):
        post = Post.objects.create(
            author=author,
            title=title,
            description=description,
            contentType=contentType,
            content=content,
            visibility=visibility
        )
        # force id_url
        post.id_url = f"http://localhost:8000/api/authors/{author.id}/posts/{post.id}"
        post.save()
        return post

    return _create_post


@pytest.fixture
def create_comment():
    def _create_comment(author, post, comment_text="Nice post", contentType="text/plain"):
        comment = Comment.objects.create(
            author=author,
            post=post,
            comment=comment_text,
            contentType=contentType
        )
        comment.id_url = f"http://localhost:8000/api/authors/{author.id}/commented/{comment.id}"
        comment.save()
        return comment

    return _create_comment


@pytest.fixture
def create_like():
    def _create_like(author, obj):
        like = Like.objects.create(
            author=author,
            object=obj.id_url
        )
        like.id_url = f"http://localhost:8000/api/authors/{author.id}/liked/{like.id}"
        like.save()
        return like

    return _create_like

@pytest.mark.django_db
def test_get_comments_list(api_client, create_author, create_post, create_comment):
    user, author = create_author("testuser", "password", "Test User")
    user2, author2 = create_author("testuser2", "password2", "Test User")
    post = create_post(author)
    create_comment(author, post, comment_text="Great post!")
    create_comment(author, post, comment_text="I agree!")
    create_comment(author2, post, comment_text="I agree!")

    # Endpoint: GET /api/authors/{author_serial}/posts/{post_serial}/comments
    url = f"/api/authors/{author.id}/posts/{post.id}/comments"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert "count" in response.data
    assert "src" in response.data
    assert response.data["type"] == "comments"
    assert response.data["count"] == 3
    assert len(response.data["src"]) == 3


@pytest.mark.django_db
def test_create_comment_success(api_client, create_author, create_post):
    user, author = create_author("commenter", "password", "Commenter")
    post = create_post(author)

    url = f"/api/authors/{author.id}/commented"
    data = {
        "comment": "This is a test comment.",
        "contentType": "text/plain",
        "post": post.id_url,  # post is referenced by its URL
    }
    api_client.force_authenticate(user=user)
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert "comment" in response.data
    assert response.data["comment"] == "This is a test comment."


@pytest.mark.django_db
def test_create_comment_missing_fields(api_client, create_author):
    user, author = create_author("commenter2", "password", "Commenter 2")

    url = f"/api/authors/{author.id}/commented"
    # post field not in payload
    data = {
        "comment": "Missing post field",
        "contentType": "text/plain",
    }
    api_client.force_authenticate(user=user)
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "post" in response.data


@pytest.mark.django_db
def test_get_single_comment(api_client, create_author, create_post, create_comment):
    user, author = create_author("singlecommenter", "password", "Single Commenter")
    post = create_post(author)
    comment = create_comment(author, post, comment_text="test comment")

    url = f"/api/authors/{author.id}/commented/{comment.id}"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["type"] == "comment"
    assert response.data["comment"] == "test comment"

@pytest.mark.django_db
def test_get_likes_list(api_client, create_author, create_post, create_like):
    user, author = create_author("liker", "password", "Liker")
    post = create_post(author)
    create_like(author, post)
    create_like(author, post)

    url = f"/api/authors/{author.id}/posts/{post.id}/likes"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["type"] == "likes"
    assert "count" in response.data
    assert "src" in response.data
    assert response.data["count"] == 2
    assert len(response.data["src"]) == 2


@pytest.mark.django_db
def test_get_single_like(api_client, create_author, create_post, create_like):
    user, author = create_author("singleliker", "password", "Single Liker")
    post = create_post(author)
    like = create_like(author, post)

    url = f"/api/authors/{author.id}/liked/{like.id}"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["type"] == "like"
    assert response.data["id"] == like.id_url

@pytest.mark.django_db
def test_get_single_like_fqid(api_client, create_author, create_post, create_like):
    user, author = create_author("singleliker", "password", "Single Liker")
    post = create_post(author)
    like = create_like(author, post)

    url = f"/api/liked/{like.id_url}"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["type"] == "like"
    assert response.data["author"]["id"] == author.id_url


@pytest.mark.django_db
def test_create_like_success(api_client, create_author, create_post):
    user, author = create_author("liker2", "password", "Liker 2")
    post = create_post(author)
    url = "/api/like"
    data = {
        "author_id": author.id,
        "object": post.id_url
    }
    api_client.force_authenticate(user=user)
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert "message" in response.data
    assert response.data["message"] == "Like created successfully"


@pytest.mark.django_db
def test_create_like_missing_fields(api_client):
    url = "/api/like"
    data = {
        "author_id": 1
    }
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data


@pytest.mark.django_db
def test_delete_like_success(api_client, create_author, create_post, create_like):
    user, author = create_author("liker3", "password", "Liker 3")
    post = create_post(author)
    like = create_like(author, post)
    data = {
        "author_id": author.id,
        "object": post.id_url
    }
    url = "/api/like"
    api_client.force_authenticate(user=user)
    response = api_client.delete(url, data, format="json")

    assert response.status_code == status.HTTP_202_ACCEPTED
    with pytest.raises(Like.DoesNotExist):
        Like.objects.get(id=like.id)


@pytest.mark.django_db
def test_delete_like_not_found(api_client, create_author, create_post):
    user, author = create_author("liker4", "password", "Liker 4")
    post = create_post(author)
    url = "/api/like"
    data = {
        "author_id": author.id,
        "object": post.id_url
    }
    api_client.force_authenticate(user=user)
    response = api_client.delete(url, data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_like_comment_nested_paginated_likes(api_client, create_author, create_post, create_comment):
    user, author = create_author("commentliker", "password", "Comment Liker")
    post = create_post(author)
    comment = create_comment(author, post, comment_text="Test comment for like")

    like_url = "/api/like"
    like_data = {
        "author_id": author.id,
        "object": comment.id_url
    }
    api_client.force_authenticate(user=user)
    like_response = api_client.post(like_url, like_data)
    assert like_response.status_code == status.HTTP_201_CREATED

    user2, author2 = create_author("commentliker2", "password2", "Comment Liker2")
    api_client.force_authenticate(user=user2)
    like_data2 = {
        "author_id": author2.id,
        "object": comment.id_url
    }
    api_client.post(like_url, like_data2)

    comment_url = f"/api/authors/{author.id}/commented/{comment.id}"
    response = api_client.get(comment_url)
    assert response.status_code == status.HTTP_200_OK

    likes_data = response.data.get("likes")
    assert likes_data is not None

    assert "count" in likes_data
    count = likes_data["count"]
    assert count == 2

    results = likes_data.get("src")
    assert results is not None
    assert len(results) == 2

    like1 = results[0]
    assert like1.get("type") == "like"
    assert like1["author"]["id"] == author.id_url

    like2 = results[1]
    assert like2.get("type") == "like"
    assert like2["author"]["id"] == author2.id_url