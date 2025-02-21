from urllib.parse import unquote

from django.http.response import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .serializers import PostSerializer
from rest_framework.generics import ListAPIView

from ..authors.models import Author
from ..utils.paginators import PostsPaginator


# Create your views here.
@api_view(["GET"])
def get_post(request, url_id):
    decoded_url = unquote(url_id)
    try:
        post = Post.objects.get(id_url=decoded_url)
        if post.visibility == 'FRIENDS':
            # validate the user is friend of author or is author
            print("Are Friends")
        elif post.visibility != 'PUBLIC':
            raise Http404
    except Post.DoesNotExist:
        raise Http404

    serializer = PostSerializer(post)
    return Response(serializer.data)

def get_author_post(request, auth_id, post_id):
    try:
        author = Author.objects.get(id=auth_id)
        if author.state != "ACTIVE":
            return Response({"error": "Author not found"}, status=404)
    except Author.DoesNotExist:
        return Response({"error": "Author not found"}, status=404)

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=404)

    if post.visibility == 'PUBLIC' or post.visibility == 'UNLISTED':
        serializer = PostSerializer(post)
        return Response(serializer.data, status=200)
    elif post.visibility == 'FRIENDS':
        # Need to check for friends validation
        print("Are Friends")
        serializer = PostSerializer(post)
        return Response(serializer.data, status=200)
    else:
        if request.user.is_authenticated and request.user.is_staff:
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

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

    if request.user.author_profile.id != auth_id:
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

# @api_view(["GET"])
# def get_posts(request):
#     try:
#         posts = Post.objects.all()
#     except Post.DoesNotExist:
#         return Response({})
#     serializer = PostSerializer(posts, many=True)
#     return Response(serializer.data)

class PostListCreateView(ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PostsPaginator

    def get_queryset(self):
        auth_id = self.kwargs.get('auth_id')
        queryset = Post.objects.filter(author_id=auth_id)
        queryset = queryset.exclude(visibility='DELETED')

        if not self.request.user.is_authenticated:
            return  queryset.filter(visibility='PUBLIC')
        elif self.request.user.author_profile.id == auth_id and not self.request.user.is_staff:
            return queryset
        elif self.request.user.is_staff:
            return Post.objects.filter(author_id=auth_id)
        elif self.request.user.author_profile.id != auth_id:
            # need to validate based on friends and followers
            return queryset

    def post(self, request, *args, **kwargs):
        auth_id = self.kwargs.get('auth_id')

        if not self.request.user.is_authenticated or auth_id != self.request.user.author_profile.id:
            return Response(status=401)
        elif self.request.user.author_profile.id == auth_id:
            serializer = PostSerializer(data=request.data, context={'auth_id': auth_id})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            else:
                return Response(serializer.errors, status=400)
