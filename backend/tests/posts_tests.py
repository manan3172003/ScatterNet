import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from urllib.parse import quote
from apps.posts.models import Post
from apps.authors.models import Author

@pytest.mark.django_db
def test_get_post_when_table_is_empty():
    client = APIClient()

    # test data setup
    # Nothing in table

    # API Call
    pathvar = quote("http://localhost:8000/api/posts/1", safe='')

    url = "http://localhost:8000/api/posts/" + pathvar + "/"
    response = client.get(url)

    # Checks
    assert response.status_code == status.HTTP_404_NOT_FOUND

