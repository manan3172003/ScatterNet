import pytest
from unittest.mock import patch, MagicMock
from apps.utils.helper import fetch_remote_friends, fetch_all_remote_users, send_object

from apps.follow.models import Follow
from apps.authors.models import Author

class FakeThread:
    def __init__(self, target, daemon):
        self._target = target

    def start(self):
        self._target()

    def join(self):
        pass

@pytest.fixture
def create_author():
    def _create_author(username, password='pass', is_local=True, state="ACTIVE", host="http://localhost:8000"):
        author = Author.objects.create(
            username=username,
            state=state,
            is_local=is_local,
            host=host,
        )
        author.id_url = f"{host}/api/authors/{author.id}"
        author.page = f"{host}/authors/{author.id}"
        if author.is_local:
            author.password = password
        author.save()
        return author
    return _create_author

@pytest.fixture
def create_follow():
    def _create_follow(actor, target, is_pending=False):
        follow = Follow.objects.create(actor=actor, object=target)
        follow.isPending = is_pending
        follow.save()
        return follow
    return _create_follow


@pytest.mark.django_db
def test_fetch_remote_friends(create_author, create_follow):
    author = create_author("Author")
    remote1 = create_author("Remote 1", is_local=False)
    remote2 = create_author("Remote 2", is_local=False)
    remote3 = create_author("Remote 3", is_local=False)

    # build friendship between author and remote 1 n author and remote 2
    create_follow(actor=author, target=remote1, is_pending=False)
    create_follow(actor=remote1, target=author, is_pending=False)
    create_follow(actor=author, target=remote2, is_pending=False)
    create_follow(actor=remote2, target=author, is_pending=False)

    #this is a one way follow
    create_follow(actor=remote3, target=author, is_pending=False)

    friends = list(fetch_remote_friends(author))
    assert remote1 in friends
    assert remote2 in friends
    assert remote3 not in friends


@pytest.mark.django_db
def test_fetch_all_remote_users(create_author):
    remote1 = create_author("Remote 1", is_local=False, state="ACTIVE")
    remote2 = create_author("Remote 2", is_local=False, state="ACTIVE")
    local_author = create_author("Local", is_local=True, state="ACTIVE")
    all_remote = list(fetch_all_remote_users())
    assert remote1 in all_remote
    assert remote2 in all_remote
    assert local_author not in all_remote

#mock object for response
def dummy_response(text):
    response = MagicMock()
    response.text = text
    return response


@patch("apps.utils.helper.threading.Thread", new=FakeThread)
@patch("apps.utils.helper.request", side_effect=lambda *args, **kwargs: dummy_response("Success"))
@patch("apps.utils.helper.Host.objects.get")
def test_send_object(mock_host_get, mock_request):
    dummy_host = MagicMock()
    dummy_host.username = "user"
    dummy_host.password = "pass"
    mock_host_get.return_value = dummy_host


    remote1 = MagicMock()
    remote1.host = "http://remote1.com"
    remote1.id_url = "http://remote1.com/api/authors/remote1_id"
    remote2 = MagicMock()
    remote2.host = "http://remote2.com"
    remote2.id_url = "http://remote2.com/api/authors/remote2_id"

    payload = {"key": "value"}
    send_object(payload, [remote1, remote2])

    assert mock_request.call_count == 2

    called_urls = [call.kwargs.get("url") for call in mock_request.call_args_list]
    expected_url1 = f"{remote1.id_url}/inbox/"
    expected_url2 = f"{remote2.id_url}/inbox/"

    assert expected_url1 in called_urls
    assert expected_url2 in called_urls