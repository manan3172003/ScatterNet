from urllib.parse import unquote

from django.http.response import Http404
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Like, Comment
from .serializers import PostSerializer, LikeSerializer, CommentSerializer, CommentCreateSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView


from ..authors.models import Author
from ..utils.paginators import PostsPaginator, LikesPaginator, CommentsPaginator
from ..utils.helper import are_friends, follows


# Create your views here.
@api_view(["GET"])
def get_post(request, url_id):
    context = {'request': request}
    decoded_url = unquote(url_id)
    try:
        post = Post.objects.get(id_url=decoded_url)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

    if post.visibility in ["PUBLIC", "UNLISTED"]:
        return Response(PostSerializer(post, context=context).data, status=status.HTTP_200_OK)

    if request.user.is_authenticated:
        if request.user.is_staff:
            return Response(PostSerializer(post, context=context).data, status=status.HTTP_200_OK)
        elif post.visibility == "DELETED":
            return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)
        elif request.user.author_profile.id == post.author.id or are_friends(request.user.author_profile.id, post.author.id):
            return Response(PostSerializer(post, context=context).data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'This post cannot be accessed.'}
                            , status=status.HTTP_403_FORBIDDEN)
    elif post.visibility != "DELETED":
        return Response({'error': 'This post cannot be accessed.'}
                        , status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

def get_author_post(request, auth_id, post_id):
    context = {'request': request}
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
        return Response(PostSerializer(post, context=context).data, status=status.HTTP_200_OK)

    if request.user.is_authenticated:
        if request.user.is_staff:
            return Response(PostSerializer(post, context=context).data, status=status.HTTP_200_OK)
        elif post.visibility == "DELETED":
            return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)
        elif request.user.author_profile.id == post.author.id or are_friends(request.user.author_profile.id, post.author.id):
            return Response(PostSerializer(post, context=context).data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'This post cannot be accessed.'})
    elif post.visibility != "DELETED":
        return Response({'error': 'This post cannot be accessed.'})
    else:
        return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)


def put_author_post(request, auth_id, post_id):
    context = {'request': request}
    if not request.user.is_authenticated:
        return Response({'error': 'Need to be logged in to update a post'}, status=status.HTTP_401_UNAUTHORIZED)

    if request.user.author_profile.id != auth_id and not request.user.is_staff:
        return Response({'error': 'Incorrect author'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = PostSerializer(post, data=request.data, partial=True, context=context)
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
            context = {'auth_id': auth_id, 'request': request}
            serializer = PostSerializer(data=request.data, context=context)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


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

class CommentedListCreateView(ListCreateAPIView):
    pagination_class = CommentsPaginator

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommentSerializer
        else:
            return CommentCreateSerializer

    def get_queryset(self):
        if 'author_serial' in self.kwargs:
            return Comment.objects.filter(author__id=self.kwargs.get("author_serial"))
        elif 'author_fqid' in self.kwargs:
            return Comment.objects.filter(author__id_url=self.kwargs.get("author_fqid"))

    def post(self, request, *args, **kwargs):
        if 'author_fqid' in self.kwargs:
            return Response({"error": "POST is not allowed on this endpoint."},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().post(request, *args, **kwargs)


class CommentRetrieveView(RetrieveAPIView):
    serializer_class = CommentSerializer

    def get_object(self):
        if 'comment_serial' in self.kwargs:
            author_serial = self.kwargs.get('author_serial')
            comment_serial = self.kwargs.get('comment_serial')
            author = get_object_or_404(Author, pk=author_serial)
            return get_object_or_404(Comment, author=author, pk=comment_serial)

        elif 'comment_fqid' in self.kwargs:
            comment_fqid = self.kwargs.get('comment_fqid')
            return get_object_or_404(Comment, id_url=comment_fqid)