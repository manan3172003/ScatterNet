from ..follow.models import Follow

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