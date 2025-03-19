from ..utils.helper import are_friends

def has_post_access(user, post):
    if post.visibility in ['PUBLIC', 'UNLISTED']:
        return True

    if user.is_authenticated:
        if user.is_staff:
            return True
        elif post.visibility == 'DELETED':
            return False
        elif user.author_profile.id == post.author.id or are_friends(user.author_profile.id, post.author.id):
            return True

    return False

def can_access_comment(comment, request):
    """
    checks:
      - if the post is public or unlisted, anyone can see the comment.
      - if the user is authenticated:
            - node admin can access any comment.
            - if deleted post, then the comment is not accessible to anyone.
            - if the user is the comment’s author or is friends with the comment’s author, allow access.
      - Otherwise, access is denied.
    """
    post_visibility = comment.post.visibility
    if post_visibility in ["PUBLIC", "UNLISTED"]:
        return True
    if request.user.is_authenticated:
        if request.user.is_staff:
            return True
        elif post_visibility == "DELETED":
            return False
        elif request.user.author_profile.id == comment.author.id or are_friends(request.user.author_profile.id, comment.author.id):
            return True
    return False