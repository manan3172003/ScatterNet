from urllib.parse import unquote

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .serializers import PostSerializer
from rest_framework.generics import ListAPIView

from ..authors.models import Author
from ..utils.helper import are_friends, follows
from ..utils.paginators import PostsPaginator


# Create your views here.
@api_view(["GET"])
def get_post(request, url_id):
    decoded_url = unquote(url_id)
    try:
        post = Post.objects.get(id_url=decoded_url)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

    if post.visibility in ["PUBLIC", "UNLISTED"]:
        return Response(PostSerializer(post).data, status=status.HTTP_200_OK)

    if request.user.is_authenticated:
        if request.user.is_staff:
            return Response(PostSerializer(post).data, status=status.HTTP_200_OK)
        elif post.visibility == "DELETED":
            return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)
        elif request.user.author_profile.id == post.author.id or are_friends(request.user.author_profile.id, post.author.id):
            return Response(PostSerializer(post).data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'This post cannot be accessed.'}
                            , status=status.HTTP_403_FORBIDDEN)
    elif post.visibility != "DELETED":
        return Response({'error': 'This post cannot be accessed.'}
                        , status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

def get_author_post(request, auth_id, post_id):
    try:
        author = Author.objects.get(id=auth_id)
        if author.state != "ACTIVE":
            return Response({"error": "Author not found"}, status=status.HTTP_404_NOT_FOUND)
    except Author.DoesNotExist:
        return Response({"error": "Author not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    if post.visibility in ["PUBLIC", "UNLISTED"]:
        return Response(PostSerializer(post).data, status=status.HTTP_200_OK)

    if request.user.is_authenticated:
        if request.user.is_staff:
            return Response(PostSerializer(post).data, status=status.HTTP_200_OK)
        elif post.visibility == "DELETED":
            return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)
        elif request.user.author_profile.id == post.author.id or are_friends(request.user.author_profile.id, post.author.id):
            return Response(PostSerializer(post).data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'This post cannot be accessed.'})
    elif post.visibility != "DELETED":
        return Response({'error': 'This post cannot be accessed.'})
    else:
        return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)


def put_author_post(request, auth_id, post_id):
    if not request.user.is_authenticated:
        return Response({'error': 'Need to be logged in to update a post'}, status=status.HTTP_401_UNAUTHORIZED)

    if request.user.author_profile.id != auth_id and not request.user.is_staff:
        return Response({'error': 'Incorrect author'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = PostSerializer(post, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def delete_author_post(request, auth_id, post_id):
    if not request.user.is_authenticated:
        return Response({'error': 'Need to be logged in to delete a post'}, status=status.HTTP_401_UNAUTHORIZED)

    if request.user.author_profile.id != auth_id and not request.user.is_staff:
        return Response({'error': 'Incorrect author'}, status=status.HTTP_403_FORBIDDEN)

    try:
        post = Post.objects.get(id=post_id, author__id=auth_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    post.visibility = 'DELETED'
    post.save()

    return Response({'message': 'Post deleted'}, status=status.HTTP_200_OK)

@api_view(["GET", "PUT", "DELETE"])
def author_post(request, auth_id, post_id):
    if request.method == 'GET':
        return get_author_post(request, auth_id, post_id)
    elif request.method == 'PUT':
        return put_author_post(request, auth_id, post_id)
    elif request.method == 'DELETE':
        return delete_author_post(request, auth_id, post_id)


class PostListCreateView(ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PostsPaginator

    def get_queryset(self):
        auth_id = self.kwargs.get('auth_id')
        queryset = Post.objects.filter(author_id=auth_id)
        queryset = queryset.exclude(visibility='DELETED')
        queryset = queryset.order_by('-published')

        if not self.request.user.is_authenticated:
            return  queryset.filter(visibility='PUBLIC')

        elif self.request.user.author_profile.id == auth_id and not self.request.user.is_staff:
            return queryset
        elif self.request.user.is_staff:
            return Post.objects.filter(author_id=auth_id).order_by('-published')
        elif self.request.user.author_profile.id != auth_id:
            if are_friends(self.request.user.author_profile.id, auth_id):
                return queryset.filter(visibility='FRIENDS')
            elif follows(self.request.user.author_profile.id, auth_id):
                return queryset.filter(visibility__in=['PUBLIC', 'UNLISTED'])
            else:
                return queryset.filter(visibility='PUBLIC')


    def post(self, request, *args, **kwargs):
        auth_id = self.kwargs.get('auth_id')

        if not self.request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        elif self.request.user.author_profile.id == auth_id or self.request.user.author_profile.is_staff:
            serializer = PostSerializer(data=request.data, context={'auth_id': auth_id})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
