from ..follow.models import Follow
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