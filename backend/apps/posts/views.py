from urllib.parse import unquote

from django.http.response import Http404
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Like, Comment
from .serializers import PostSerializer, LikeSerializer, CommentSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView


from ..authors.models import Author
from ..utils.paginators import PostsPaginator, LikesPaginator, CommentsPaginator


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


class LikesListView(ListAPIView):
    serializer_class = LikeSerializer
    pagination_class = LikesPaginator

    def get_queryset(self):
        author_serial = self.kwargs.get('author_serial')
        post_serial = self.kwargs.get('post_serial')
        comment_fqid = self.kwargs.get('comment_fqid')

        if author_serial and post_serial:
            if comment_fqid: #implement comment first
                comment = get_object_or_404(Comment, id_url=comment_fqid)
                queryset = Like.objects.filter(object=comment.id_url)
                return queryset

            else:
                author = get_object_or_404(Author, pk=author_serial)
                post = get_object_or_404(Post, pk=post_serial, author_id=author.id)
                queryset = Like.objects.filter(object=post.id_url)
                return queryset

        elif author_serial:
            author = get_object_or_404(Author, pk=author_serial)
            queryset = Like.objects.filter(author_id=author.id)
            return queryset

        author_fqid = self.kwargs.get('author_fqid')
        if author_fqid:
            author = get_object_or_404(Author, id_url=author_fqid)
            queryset = Like.objects.filter(author_id=author.id)
            return queryset

        post_fqid = self.kwargs.get('post_fqid')

        if post_fqid:
            post = get_object_or_404(Post, id_url=post_fqid)
            queryset = Like.objects.filter(object=post.id)
            return queryset

class LikeRetrieveView(RetrieveAPIView):
    serializer_class = LikeSerializer

    def get_queryset(self):
        like_fqid = self.kwargs.get('like_fqid')
        if like_fqid:
            queryset = Like.objects.filter(id_url=like_fqid)
            return queryset
        else:
            author_serial = self.kwargs.get('author_serial')
            like_serial = self.kwargs.get('like_serial')
            queryset = Like.objects.filter(author_id=author_serial, pk=like_serial)
            return queryset


def post_like(author_id, object_url):
    author = get_object_or_404(Author, id=author_id)
    created_like = Like.objects.create(
        author=author,
        object=object_url,
    )
    created_like.id_url = "http://localhost:8000/authors/{}/liked/{}".format(author.id, created_like.id)
    created_like.save()

    return Response({'message': 'Like created successfully'}, status=status.HTTP_201_CREATED)


def delete_like(author_id, object_url):
    like = get_object_or_404(Like, author_id=author_id, object=object_url)
    like.delete()
    return Response({'message': 'Like deleted successfully'}, status=status.HTTP_202_ACCEPTED)


@swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['author_id', 'object'],
            properties={
                'author_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="ID of the Author performing the like action."
                ),
                'object': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="URL ID of the Object (Post/Comment) that was liked."
                )
            }
        ),
        methods=['post', 'delete'],
    )
@api_view(['POST','DELETE'])
def create_or_delete_like(request):
    author_id = request.data.get('author_id')
    object_url = request.data.get('object')
    if not author_id:
        return Response({'error': 'No author id found with the like.'}, status=status.HTTP_400_BAD_REQUEST)
    if not object_url:
        return Response({'error': 'No object url present in request, cannot identify what was liked.'},
                        status=status.HTTP_400_BAD_REQUEST)

    if request.method == "POST":
        return post_like(author_id, object_url)
    else:
        return delete_like(author_id, object_url)


class CommentsListView(ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = CommentsPaginator

    def get_queryset(self):
        author_serial = self.kwargs.get('author_serial')
        post_serial = self.kwargs.get('post_serial')

        if author_serial and post_serial:
            author = get_object_or_404(Author, id=author_serial)
            post = get_object_or_404(Post, author=author, id=post_serial)
            queryset = Comment.objects.filter(post=post)
            return queryset

        post_fqid = self.kwargs.get('post_fqid')
        if post_fqid:
            post = get_object_or_404(Post, id_url=post_fqid)
            queryset = Comment.objects.filter(post=post)
            return queryset

# TODO: URL: ://service/api/authors/{AUTHOR_SERIAL}/post/{POST_SERIAL}/comment/{REMOTE_COMMENT_FQID}