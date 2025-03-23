from ..follow.models import Follow
from ..authors.models import Author
from requests import request
from requests.auth import HTTPBasicAuth
from dodgerblue.settings import DODGERBLUE_NODE_PASSWORD, DODGERBLUE_NODE_USERNAME
import json
import heapq

def are_friends(author1_id, author2_id):
    try:
        follows_1_2 = Follow.objects.get(actor_id=author1_id, object_id=author2_id, isPending=False)
        follows_2_1 = Follow.objects.get(actor_id=author2_id, object_id=author1_id, isPending=False)
        return True
    except Follow.DoesNotExist:
        return False

def follows(author1_id, author2_id):
    try:
        follows = Follow.objects.get(actor_id=author1_id, object_id=author2_id, isPending=False)
        return True
    except Follow.DoesNotExist:
        return False

def merge_sorted_post_lists(*lists):
    """
    Perform a k-way merge on the sorted lists of posts using their published date.
    """
    return heapq.merge(*lists, key=lambda post: post.published, reverse=True)

#the is_local = false ensures, we dont send the post back to ourselves
def fetch_remote_followers(author):
    authors_followers = Follow.objects.filter(object=author, isPending=False).values_list('actor', flat=True)
    followers = Author.objects.filter(id__in=authors_followers, state="ACTIVE", is_local = False)
    return followers

def fetch_remote_friends(author):
    author = Author.objects.filter(object=author, state="ACTIVE")
    authors_following = Follow.objects.filter(actor=author, isPending=False).values_list('object', flat=True)
    authors_followers = Follow.objects.filter(object=author, isPending=False).values_list('actor', flat=True)
    authors_friends = set(authors_following).intersection(authors_followers)
    friends = Author.objects.filter(id__in=authors_friends, is_local=False)
    return friends

def fetch_all_remote_users():
    remote_authors = Author.objects.filter(state="ACTIVE", is_local=False)
    return remote_authors

def send_object(payload, remote_authors):
    payload = json.dumps(payload)
    print(payload)
    print("payload:", payload)
    headers = {'Content-Type': 'application/json'}
    for remote_author in remote_authors:
        inbox_url = f"{remote_author.host}/api/authors/{remote_author.id_url}/inbox"
        resp = request(method="POST",
                url=inbox_url,
                data=payload,
                auth=HTTPBasicAuth("8000user", "8000user"),
                headers=headers
        )
        print("This is the fuckin response:", resp.text)
