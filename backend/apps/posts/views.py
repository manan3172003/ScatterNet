# TODO: Cleanup this file for example make validations cleaner and replace try excepts with get_object_or_404
from urllib.parse import unquote
from django.http import Http404
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Like, Comment
from .serializers import PostSerializer, LikeSerializer, CommentSerializer, CommentCreateSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView


from ..authors.models import Author
from ..utils.paginators import PostsPaginator, LikesPaginator, CommentsPaginator
from ..utils.helper import are_friends, follows, merge_sorted_post_lists

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'url_id',
            openapi.IN_PATH,
            description="Encoded FQID of the post.",
            type=openapi.TYPE_STRING
        )
    ],
    responses={
        200: openapi.Response('OK', PostSerializer),
        403: 'Access forbidden to the post',
        404: 'Post not found'
    }
)
@api_view(["GET"])
def get_post(request, url_id):
    """
    http://{node}/api/posts/{POST_FQID}

    GETs a post with id_url POST_FQID if the caller has permissions
    """
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

"""
http://{node}/api/authors/{AUTHOR_SERIAL}/posts/{POST_SERIAL}

GETs a post with id POST_SERIAL belonging to author with id AUTHOR_SERIAL
if the caller has permissions
"""

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


"""
http://{node}/api/authors/{AUTHOR_SERIAL}/posts/{POST_SERIAL}

PUTs a post with id POST_SERIAL belonging to author with id AUTHOR_SERIAL
if the caller has permissions (Caller needs to be author AUTHOR_SERIAL or node admin)
"""

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

"""
http://{node}/api/authors/{AUTHOR_SERIAL}/posts/{POST_SERIAL}

DELETEs a post with id POST_SERIAL belonging to author with id AUTHOR_SERIAL
if the caller has permissions (Caller needs to be author AUTHOR_SERIAL or node admin)
"""

def delete_author_post(request, auth_id, post_id):
    if not request.user.is_authenticated:
        return Response({'error': 'Need to be logged in to delete a post'}, status=status.HTTP_401_UNAUTHORIZED)

    if request.user.author_profile.id != auth_id and not request.user.is_staff:
        # TODO: Fix error message to something like "You cannot edit this post unless you made it or you are a Node Admin"
        return Response({'error': 'Incorrect author'}, status=status.HTTP_403_FORBIDDEN)

    try:
        post = Post.objects.get(id=post_id, author__id=auth_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    post.visibility = 'DELETED'
    post.save()

    return Response({'message': 'Post deleted'}, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response('OK', PostSerializer),
        404: 'Post not found',
        403: 'Access forbidden'
    }
)
@swagger_auto_schema(
    method='put',
    request_body=PostSerializer,
    responses={
        200: openapi.Response('OK', PostSerializer),
        400: 'Bad request due to validation errors',
        401: 'Unauthorized',
        404: 'Post not found'
    }
)
@swagger_auto_schema(
    method='delete',
    responses={
        200: 'Post deleted',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Post not found'
    }
)
@api_view(["GET", "PUT", "DELETE"])
def author_post(request, auth_id, post_id):
    if request.method == 'GET':
        return get_author_post(request, auth_id, post_id)
    elif request.method == 'PUT':
        return put_author_post(request, auth_id, post_id)
    elif request.method == 'DELETE':
        return delete_author_post(request, auth_id, post_id)

"""
Helper function which returns the list of posts belonging to author with id AUTHOR_SERIAL
Shows the posts of author with id AUTHOR_SERIAL to the caller if the caller has permissions
"""
def filter_author_post(request, auth_id):
    queryset = Post.objects.filter(author_id=auth_id)
    queryset = queryset.exclude(visibility='DELETED')
    queryset = queryset.order_by('-published')

    if not request.user.is_authenticated:
        return queryset.filter(visibility='PUBLIC')

    elif request.user.author_profile.id == auth_id and not request.user.is_staff:
        return queryset
    elif request.user.is_staff:
        return Post.objects.filter(author_id=auth_id).order_by('-published')
    elif request.user.author_profile.id != auth_id:
        if are_friends(request.user.author_profile.id, auth_id):
            return queryset
        elif follows(request.user.author_profile.id, auth_id):
            return queryset.filter(visibility__in=['PUBLIC', 'UNLISTED'])
        else:
            return queryset.filter(visibility='PUBLIC')

"""
http://{node}/api/authors/{AUTHOR_SERIAL}/posts

GET calls the above helper function
POST creates a new post for author with id AUTHOR_SERIAL if the caller has permissions
"""
class PostListCreateView(ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PostsPaginator

    def get_queryset(self):
        auth_id = self.kwargs.get('auth_id')
        return filter_author_post(self.request, auth_id)

    def post(self, request, *args, **kwargs):
        auth_id = self.kwargs.get('auth_id')

        if not self.request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        elif self.request.user.author_profile.id == auth_id or self.request.user.is_staff:
            context = {'auth_id': auth_id, 'request': request}
            serializer = PostSerializer(data=request.data, context=context)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

"""
http://{node}/api/posts

GET calls the above helper function on every ACTIVE author in DB
so we can get a stream of posts in order of latest to earliest published date
"""
class StreamListView(ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PostsPaginator

    def get_queryset(self):
        authors = Author.objects.filter(state="ACTIVE")
        author_posts = []
        for author in authors:
            author_posts.append(list(filter_author_post(self.request, author.id)))

        merged_posts = list(merge_sorted_post_lists(*author_posts))
        return merged_posts

"""
http://{node}/api/posts/{post_fqid}/image
GETs an image post
"""
class ImagePostsView(RetrieveAPIView):
    serializer_class = PostSerializer

    def helper_filter(self, post):
        # Check if the post belongs to the author and is of image content type
        content_types = ['application/base64', 'image/png;base64', 'image/jpeg;base64']
        if post.contentType in content_types:
            # Verify the user has access to this post
            queryset = filter_author_post(self.request, post.author_id)
            if queryset.filter(id_url=post.id_url).exists():
                return post
            else:
                raise PermissionDenied({'error': 'You do not have permission to view this post.'})
        else:
            raise NotFound({'error': 'This post is not an image post.'})

    def get_object(self):
        if 'post_fqid' in self.kwargs:
            post_fqid = self.kwargs['post_fqid']
            # Get the post or return a 404 if it doesn't exist
            post = get_object_or_404(Post, id_url=post_fqid)
            return self.helper_filter(post)


        elif 'author_serial' in self.kwargs and 'post_serial' in self.kwargs:
            author_fqid = self.kwargs['author_serial']
            post_serial = self.kwargs['post_serial']
            post = get_object_or_404(Post, id=post_serial)
            return self.helper_filter(post)


class LikesListView(ListAPIView):
    """
    View to retrieve a collection of paginated likes
    the body is a likes object, with the src list containing a single like object

    Methods:
        GET
    URL:
        /api/authors/{author_serial: int}/posts/{post_serial: int}/comments/{comment_fqid: path}/likes
        /api/authors/{author_serial: int}/posts/{post_serial: int}/likes
        /api/authors/{author_serial: int}/liked
        /api/authors/{author_fqid: path}/liked
        /api/posts/{post_fqid: path}/likes

    """
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
    """
    View that only retrieves a single Like object based on either the api/liked/id_url path or
    api/author_serial/liked/like_serial

    Method:
        GET
    URL:
        /api/authors/{author_serial: int}/liked/{like_serial: int}
        /api/liked/{like_fqid: path}
    """
    serializer_class = LikeSerializer

    def get_object(self):
        like_fqid = self.kwargs.get('like_fqid')
        if like_fqid:
            return get_object_or_404(Like, id_url=like_fqid)
        else:
            author_serial = self.kwargs.get('author_serial')
            like_serial = self.kwargs.get('like_serial')
            return get_object_or_404(Like, author_id=author_serial, pk=like_serial)


def post_like(author_id, object_url):
    author = get_object_or_404(Author, id=author_id)

    created_like, created_success = Like.objects.get_or_create(author=author, object=object_url)

    if not created_success:
        return Response({'message': 'Like already exists'}, status=status.HTTP_400_BAD_REQUEST)

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
                    description="FQID of the Object (Post/Comment) that was liked."
                )
            }
        ),
        methods=['post', 'delete'],
    )
@api_view(['POST','DELETE'])
def create_or_delete_like(request):
    """
    Internal endpoint that facilitates liking an object or deleting a liked object

    Delete hasn't been mentioned in the API spec yet so it might be removed in the future if required

    Methods:
        POST
        DELETE
    URL:
        /api/like
    """
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


class CommentsListView(ListAPIView):
    """
    Similar stuff to likes above, this returns a Comments collection, with also a likes section that is paginated in
    the layer underneath

    Methods:
        GET
    URL:
        /api/authors/{author_serial: int}/posts/{post_serial: int}/comments
        /api/posts/{post_fqid: path}/comments

    """
    serializer_class = CommentSerializer
    pagination_class = CommentsPaginator

    def get_post(self):
        if 'author_serial' in self.kwargs and 'post_serial' in self.kwargs:
            author = get_object_or_404(Author, id=self.kwargs.get('author_serial'))
            return get_object_or_404(Post, author=author, id=self.kwargs.get('post_serial'))
        elif 'post_fqid' in self.kwargs:
            return get_object_or_404(Post, id_url=self.kwargs.get('post_fqid'))
        else:
            raise Http404("Post not found.")

    def get_queryset(self):
        post = self.get_post()
        if post.visibility in ["PUBLIC", "UNLISTED"]:
            return Comment.objects.filter(post=post)
        if self.request.user.is_authenticated:
            if (self.request.user.is_staff or self.request.user.author_profile.id == post.author.id or
                    are_friends(self.request.user.author_profile.id, post.author.id)):
                return Comment.objects.filter(post=post)
        raise Http404("Post not found.")

# TODO: URL: ://service/api/authors/{AUTHOR_SERIAL}/post/{POST_SERIAL}/comment/{REMOTE_COMMENT_FQID}

class CommentedListCreateView(ListCreateAPIView):
    """
    APIView to both, list a collection and create a comment on that endpoint
    Method:
        GET
        POST
    URL:
        /api/authors/{author_serial: int}/commented
        /api/authors/{author_fqid: path}/commented (GET ONLY)
    """
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


        #validate to check whether user can comment on this post
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required to post a comment."},
                            status=status.HTTP_401_UNAUTHORIZED)

        post_id_url = request.data.get('post')
        post = get_object_or_404(Post, id_url=post_id_url)

        if request.user.is_authenticated:
            if request.user.is_staff or post.visibility in ["PUBLIC", "UNLISTED"]:
                return super().post(request, *args, **kwargs)
            elif post.visibility == "DELETED":
                return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)
            elif (request.user.author_profile.id == post.author.id or
                  are_friends(request.user.author_profile.id, post.author.id)):
                return super().post(request, *args, **kwargs)
            else:
                return Response({'error': 'You are not allowed to comment on this post.'},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'error': 'You are not logged in to comment.'},
                            status=status.HTTP_403_FORBIDDEN)

        return super().post(request, *args, **kwargs)


class CommentRetrieveView(RetrieveAPIView):
    """
    This view to return a single comment object

    Method:
        GET
    URL:
        /api/authors/{author_serial: int}/commented/{comment_serial: int}
        /api/commented/{comment_fqid: path}
    """
    serializer_class = CommentSerializer

    def get_object(self):
        if 'comment_serial' in self.kwargs:
            author_serial = self.kwargs.get('author_serial')
            comment_serial = self.kwargs.get('comment_serial')
            author = get_object_or_404(Author, pk=author_serial)
            comment = get_object_or_404(Comment, author=author, pk=comment_serial)

        elif 'comment_fqid' in self.kwargs:
            comment_fqid = self.kwargs.get('comment_fqid')
            comment = get_object_or_404(Comment, id_url=comment_fqid)

        if comment.post.visibility == 'DELETED':
            raise Http404("Comment not found.")

        if can_access_comment(comment, self.request):
            return comment
        raise Http404("Comment not found.")