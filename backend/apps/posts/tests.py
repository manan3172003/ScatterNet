from django.test import TestCase

# Create your tests here.

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from ..authors.models import Author
from .models import Post, Comment, Like, Inbox
from dodgerblue.settings import NODEHOSTNAME
import base64

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

# Posts API Tests
@pytest.mark.django_db
def test_create_post_success(api_client, create_author):
    user, author = create_author("author1", "password", "Author 1")

    url = f"/api/authors/{author.id}/posts"
    data = {
        "title": "Test Post Title",
        "description": "This is a test post",
        "contentType": "text/plain",
        "content": "This is some content for the test post.",
        "visibility": "PUBLIC"
    }
    api_client.force_authenticate(user=user)
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == "Test Post Title"
    assert response.data["description"] == "This is a test post"
    assert response.data["content"] == "This is some content for the test post."
    assert response.data["visibility"] == "PUBLIC"

@pytest.mark.django_db
def test_create_post_missing_fields(api_client, create_author):
    user, author = create_author("author2", "password", "Author 2")

    url = f"/api/authors/{author.id}/posts"
    data = {
        "title": "Test Post Title",  # Missing contentType and content
        "description": "Missing required fields"
    }
    api_client.force_authenticate(user=user)
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "contentType" in response.data
    assert "content" in response.data

@pytest.mark.django_db
def test_get_all_posts(api_client, create_author, create_post):
    user, author = create_author("author3", "password", "Author 3")
    create_post(author, title="Post 1")
    create_post(author, title="Post 2")

    url = f"/api/authors/{author.id}/posts"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert "count" in response.data
    assert response.data["count"] == 2
    assert len(response.data["src"]) == 2

@pytest.mark.django_db
def test_get_single_post(api_client, create_author, create_post):
    user, author = create_author("author4", "password", "Author 4")
    post = create_post(author, title="Single Post")

    url = f"/api/authors/{author.id}/posts/{post.id}"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["type"] == "post"
    assert response.data["title"] == "Single Post"

@pytest.mark.django_db
def test_update_post_success(api_client, create_author, create_post):
    user, author = create_author("author5", "password", "Author 5")
    post = create_post(author, title="Original Title")

    url = f"/api/authors/{author.id}/posts/{post.id}"
    updated_data = {
        "title": "Updated Title",
        "description": "Updated Description",
        "contentType": "text/plain",
        "content": "Updated content",
        "visibility": "FRIENDS"
    }
    api_client.force_authenticate(user=user)
    response = api_client.put(url, updated_data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "Updated Title"
    assert response.data["visibility"] == "FRIENDS"
    assert response.data["content"] == "Updated content"

@pytest.mark.django_db
def test_delete_post_success(api_client, create_author, create_post):
    user, author = create_author("author6", "password", "Author 6")
    post = create_post(author, title="Post to be deleted")

    url = f"/api/authors/{author.id}/posts/{post.id}"
    api_client.force_authenticate(user=user)
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_unauthorized_create_post(api_client, create_author):
    user, author = create_author("author7", "password", "Author 7")

    url = f"/api/authors/{author.id}/posts"
    data = {
        "title": "Unauthorized Post",
        "description": "Unauthorized creation attempt",
        "contentType": "text/plain",
        "content": "This should fail",
        "visibility": "PUBLIC"
    }
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_post_not_found(api_client, create_author):
    user, author = create_author("author8", "password", "Author 8")

    # Trying to access a post that does not exist
    url = f"/api/authors/{author.id}/posts/999999"  # Non-existent post ID
    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


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
def test_create_comment_missing_post(api_client, create_author):
    user, author = create_author("commenter2", "password", "Commenter 2")

    url = f"/api/authors/{author.id}/commented"
    # post field not in payload
    data = {
        "comment": "Missing post field",
        "contentType": "text/plain",
    }
    api_client.force_authenticate(user=user)
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert 'Post' in response.data['detail']


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
    user_2, author_2 = create_author("liker2", "password", "liker2")
    post = create_post(author)
    create_like(author, post)
    create_like(author_2, post)

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


@pytest.mark.django_db
def test_remote_post_creation(api_client, create_author):
    # create remote node and mark as node
    node_user, node_author = create_author("node_remote", "password", "Node Remote", state="ACTIVE")
    node_author.is_node = True
    node_author.save()
    # create inbox owner
    _, local_author = create_author("local_receiver", "password", "Local Receiver", state="ACTIVE")

    remote_post_payload = {
        "id": "http://remote.example/api/posts/1000",
        "host": "http://remote.example/api/",
        "title": "Remote Post Title",
        "description": "Remote post description",
        "contentType": "text/plain",
        "content": "Content from remote post.",
        "author": {
            "id": "http://remote.example/api/authors/2000",
            "host": "http://remote.example/api/",
            "displayName": "Remote Author",
            "profileImage": "http://remote.example/images/remote_author.png",
            "page": "http://remote.example/authors/2000",
            "type": "author"
        },
        "comments": {"src": []},
        "likes": {"src": []},
        "published": "2025-04-07T12:00:00Z",
        "visibility": "PUBLIC",
        "page": "http://remote.example/posts/1000",
        "type": "post"
    }
    credentials = base64.b64encode("node_remote:password".encode("utf-8")).decode("utf-8")
    api_client.credentials(HTTP_AUTHORIZATION=f"Basic {credentials}")

    inbox_url = f"/api/authors/{local_author.id}/inbox"
    response = api_client.post(inbox_url, remote_post_payload, format="json")

    assert response.status_code == status.HTTP_200_OK

    post = Post.objects.get(id_url=remote_post_payload["id"])
    assert post.title == "Remote Post Title"

    inbox_entry = Inbox.objects.filter(author=local_author, post=post).first()
    assert inbox_entry is not None


@pytest.mark.django_db
def test_remote_post_update(api_client, create_author):
    """
    test updating existing remote post by re-sending an updated payload
    """
    node_user, node_author = create_author("node_remote_update", "password", "Node Remote Update", state="ACTIVE")
    node_author.is_node = True
    node_author.save()
    _, local_author = create_author("local_receiver_update", "password", "Local Receiver Update", state="ACTIVE")

    remote_post_payload = {
        "id": "http://remote.example/api/posts/1001",
        "host": "http://remote.example/api/",
        "title": "Initial Remote Post Title",
        "description": "Initial description",
        "contentType": "text/plain",
        "content": "Initial remote content.",
        "author": {
            "id": "http://remote.example/api/authors/2001",
            "host": "http://remote.example/api/",
            "displayName": "Remote Author Update",
            "profileImage": "http://remote.example/images/remote_author_update.png",
            "page": "http://remote.example/authors/2001",
            "type": "author"
        },
        "comments": {"src": []},
        "likes": {"src": []},
        "published": "2025-04-07T12:00:00Z",
        "visibility": "PUBLIC",
        "page": "http://remote.example/posts/1001",
        "type": "post"
    }

    credentials = base64.b64encode("node_remote_update:password".encode("utf-8")).decode("utf-8")
    api_client.credentials(HTTP_AUTHORIZATION=f"Basic {credentials}")
    inbox_url = f"/api/authors/{local_author.id}/inbox"
    response = api_client.post(inbox_url, remote_post_payload, format="json")
    assert response.status_code == status.HTTP_200_OK

    updated_payload = remote_post_payload.copy()
    updated_payload["title"] = "Updated Remote Post Title"

    response_update = api_client.post(inbox_url, updated_payload, format="json")
    assert response_update.status_code == status.HTTP_200_OK

    post = Post.objects.get(id_url=remote_post_payload["id"])
    assert post.title == "Updated Remote Post Title"


@pytest.mark.django_db
def test_remote_post_missing_likes(api_client, create_author):
    node_user, node_author = create_author("node_missing_likes", "password", "Node Missing Likes", state="ACTIVE")
    node_author.is_node = True
    node_author.save()
    _, local_author = create_author("local_missing_likes", "password", "Local Missing Likes", state="ACTIVE")

    remote_post_payload = {
        "id": "http://remote.example/api/posts/1002",
        "host": "http://remote.example/api/",
        "title": "Remote Post Without Likes",
        "description": "Description",
        "contentType": "text/plain",
        "content": "Content",
        "author": {
            "id": "http://remote.example/api/authors/2002",
            "host": "http://remote.example/api/",
            "displayName": "Remote Author NL",
            "profileImage": "http://remote.example/images/remote_author_nl.png",
            "page": "http://remote.example/authors/2002",
            "type": "author"
        },
        "comments": {"src": []},
        # "likes" key is missing
        "published": "2025-04-07T12:00:00Z",
        "visibility": "PUBLIC",
        "page": "http://remote.example/posts/1002",
        "type": "post"
    }
    credentials = base64.b64encode("node_missing_likes:password".encode("utf-8")).decode("utf-8")
    api_client.credentials(HTTP_AUTHORIZATION=f"Basic {credentials}")
    inbox_url = f"/api/authors/{local_author.id}/inbox"
    response = api_client.post(inbox_url, remote_post_payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "No likes object" in response.data["error"]


@pytest.mark.django_db
def test_remote_comment_creation(api_client, create_author, create_post):
    node_user, node_author = create_author("node_comment", "password", "Node Comment", state="ACTIVE")
    node_author.is_node = True
    node_author.save()
    _, local_author = create_author("local_comment", "password", "Local Comment", state="ACTIVE")
    post = create_post(local_author, title="Post for Remote Comment")

    remote_comment_payload = {
        "id": "http://remote.example/api/comments/3000",
        "author": {
            "id": "http://remote.example/api/authors/2003",
            "host": "http://remote.example/api/",
            "displayName": "Remote Commenter",
            "profileImage": "http://remote.example/images/remote_commenter.png",
            "page": "http://remote.example/authors/2003",
            "type": "author"
        },
        "post": post.id_url,
        "published": "2025-04-07T12:00:00Z",
        "contentType": "text/plain",
        "comment": "This is a remote comment",
        "likes": {"src": []},
        "type": "comment"
    }

    credentials = base64.b64encode("node_comment:password".encode("utf-8")).decode("utf-8")
    api_client.credentials(HTTP_AUTHORIZATION=f"Basic {credentials}")
    inbox_url = f"/api/authors/{local_author.id}/inbox"
    response = api_client.post(inbox_url, remote_comment_payload, format="json")

    assert response.status_code == status.HTTP_200_OK
    comment = Comment.objects.get(id_url=remote_comment_payload["id"])
    assert comment.comment == "This is a remote comment"


@pytest.mark.django_db
def test_remote_like_creation(api_client, create_author, create_post):
    node_user, node_author = create_author("node_like", "password", "Node Like", state="ACTIVE")
    node_author.is_node = True
    node_author.save()
    _, local_author = create_author("local_like", "password", "Local Like", state="ACTIVE")
    post = create_post(local_author, title="Post for Remote Like")

    remote_like_payload = {
        "id": "http://remote.example/api/likes/4000",
        "author": {
            "id": "http://remote.example/api/authors/2004",
            "host": "http://remote.example/api/",
            "displayName": "Remote Liker",
            "profileImage": "http://remote.example/images/remote_liker.png",
            "page": "http://remote.example/authors/2004",
            "type": "author"
        },
        "published": "2025-04-07T12:00:00Z",
        "object": post.id_url,
        "type": "like"
    }

    credentials = base64.b64encode("node_like:password".encode("utf-8")).decode("utf-8")
    api_client.credentials(HTTP_AUTHORIZATION=f"Basic {credentials}")
    inbox_url = f"/api/authors/{local_author.id}/inbox"
    response = api_client.post(inbox_url, remote_like_payload, format="json")

    assert response.status_code == status.HTTP_200_OK
    like = Like.objects.get(id_url=remote_like_payload["id"])
    assert like.object == post.id_url


@pytest.mark.django_db
def test_inbox_invalid_auth(api_client, create_author):
    _, local_author = create_author("local_inbox", "password", "Local Inbox", state="ACTIVE")
    payload = {"type": "post"}
    url = f"/api/authors/{local_author.id}/inbox"
    response = api_client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_inbox_invalid_type(api_client, create_author):
    node_user, node_author = create_author("node_invalid", "password", "Node Invalid", state="ACTIVE")
    node_author.is_node = True
    node_author.save()
    _, local_author = create_author("local_invalid", "password", "Local Invalid", state="ACTIVE")
    payload = {"type": "invalid_type"}
    credentials = base64.b64encode("node_invalid:password".encode("utf-8")).decode("utf-8")
    api_client.credentials(HTTP_AUTHORIZATION=f"Basic {credentials}")
    url = f"/api/authors/{local_author.id}/inbox"
    response = api_client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Invalid request type" in response.data["error"]