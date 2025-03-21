from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView,CreateAPIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from urllib.parse import unquote
from .models import Author
from .serializers import AuthorSignUpSerializer, AuthorSerializer, AuthorUpdateSerializer, RemoteAuthorSerializer
from ..follow.models import Follow
from ..follow.serializers import RemoteFollowSerializer
from ..posts.models import Like, Comment, Post
from ..posts.serializers import RemoteLikeSerializer, RemoteCommentSerializer, RemotePostSerializer
from ..utils.paginators import AuthorsPaginator
from base64 import b64decode


# Create your views here.
class AuthorLoginView(APIView):
    """
    This will be the path handling all login work
    We'll take the info from the frontend and authenticate a user n use django sessions
    to sustain it

    Methods:
        GET
        POST
    URL:
        /api/authors/login
    """

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        return Response({'detail': 'CSRF cookie set.'})

    """
    So for methods using a regular APIView inheritance or the decorator, they dont
    utilize a serializer, so we need to auto enforce fields for swagger
    """
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Author's chosen username to login."
                ),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Author's password to login."
                )
            }
        )
    )
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Missing Username or Password'}, status=status.HTTP_400_BAD_REQUEST)

        auth_user = authenticate(request, username=username, password=password)
        if auth_user is not None:
            try:
                author = auth_user.author_profile
            except Author.DoesNotExist:
                return Response({'error': 'No author found'}, status=status.HTTP_404_NOT_FOUND)

            if not (author.state == 'ACTIVE'):
                return Response({'error': 'This user cannot login to the system.'},
                                    status=status.HTTP_401_UNAUTHORIZED)

            login(request, auth_user)
            response = {
                'message': 'User Logged in Successfully.',
                'user': {
                    'username': author.username,
                    'displayName': author.displayName,
                    'is_node_admin': auth_user.is_staff,
                    'author_id': author.id
                }
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Incorrect Username or Password'}, status=status.HTTP_401_UNAUTHORIZED)

class AuthorLogoutView(APIView):
    """
    This endpoint logs out a user, will be successful only if a user is logged in otherwise will complain.

    Methods:
        POST
    URL:
        /api/authors/logout
    """
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={}
        )
    )
    def post(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated:
            logout(request)
            return Response({'message': 'User logged out successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No user is logged in.'}, status=status.HTTP_401_UNAUTHORIZED)


class AuthorSignUpView(APIView):
    """
    Primary endpoint to sign up users, by default this will create all users with a PENDING
    state and the node admin needs to make a PUT call to change their state.

    Permissions for that are enforced in the PUT endpoint

    Methods:
        POST
    URL:
        /api/authors/signup
    """
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password', 'displayName'],
            properties={
                'username': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="A Unique Identifier for an Author."
                ),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Password that will be used to log in."
                ),
                'displayName': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="String that is to be displayed on an author's profile"
                )
            }
        )
    )
    def post(self, request, *args, **kwargs):
        serializer = AuthorSignUpSerializer(data=request.data)

        if serializer.is_valid():
            author = serializer.save()
            return Response({
                'message': 'User created successfully.',
                'user': {
                    'username': author.username,
                    'displayName': author.displayName,
                    'author_id': author.id,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthorsView(ListAPIView):
    """
    GET endpoint to return a collection of authors when requested.

    Methods:
        GET
    URL:
        /api/authors
    """
    serializer_class = AuthorSerializer
    pagination_class = AuthorsPaginator
    def get_queryset(self):
        queryset = Author.objects.all()
        user = self.request.user

        #filters to it such that only node admins can see all the users and everyone else just gets the active list
        if not (user and user.is_authenticated and user.is_staff):
            queryset = queryset.filter(state='ACTIVE')

        state = self.request.query_params.get('state')
        if state:
            queryset = Author.objects.filter(state=state)

        username = self.request.query_params.get('username')
        host = self.request.query_params.get('host')

        if username:
            queryset = queryset.filter(username=username)
        if host:
            queryset = queryset.filter(host=host)

        return queryset

class CheckNodeAdminChangedState(BasePermission):
    """
    Helper permission class to assist with checking node admin permissions, only does state check
    for now but we'll update that in the future to have more rigid perms
    """

    # https://www.django-rest-framework.org/api-guide/permissions/#custom-permissions neat feature
    message = "Only Node Admins are Allowed to update an Author's state."

    def has_permission(self, request, view):
        if request.method == 'PUT' and 'state' in request.data:
            return request.user.is_authenticated and request.user.is_staff
        return True

class IsNodeAdminOrSelf(BasePermission):
    """
    Allows editing an author only if the user is a node admin or the author themselves.
    """
    message = "Editing this author can only be done by the node admin or the author itself."

    def has_object_permission(self, request, view, obj):
        # only check if we are updating an author
        if request.method == 'PUT':
            # check whether its node admin
            if request.user and request.user.is_authenticated and request.user.is_staff:
                return True
            #check whether its own author
            if request.user and request.user.is_authenticated and request.user.author_profile == obj:
                return True
            return False
        return True

class AuthorRetrieveUpdateView(RetrieveUpdateAPIView):
    """
    Generic listviews can handle multiple methods, this one is to list a single instance
    or update a single instance

    Methods:
        GET
        PUT
    URL:
        /api/authors/{author_id : int}
    """
    queryset = Author.objects.all()
    http_method_names = ['get', 'put'] #explicitly only allows these two
    permission_classes = [CheckNodeAdminChangedState, IsNodeAdminOrSelf]

    def retrieve(self, request, *args, **kwargs):
        response = super(AuthorRetrieveUpdateView, self).retrieve(request, args, kwargs)
        return response

    #since we need the same endpoint, just change serializer being used based on what task we're doing
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AuthorSerializer
        else:
            return AuthorUpdateSerializer

@api_view(['GET'])
def get_author_fqid(request, id_url):
    """
    Does the same thing as the one above but instead of using a pk, it uses the FQID url indentifier

    Methods:
        GET
    URL:
        /api/authors/{author_fqid : path}
    """
    decoded_url = unquote(id_url)
    try:
        author = Author.objects.get(id_url=decoded_url)
    except Author.DoesNotExist:
        return Response({'error': 'Author does not exist with this id'}, status=status.HTTP_404_NOT_FOUND)
    serializer = AuthorSerializer(author)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@csrf_protect # https://docs.djangoproject.com/en/5.1/howto/csrf/
def get_current_user(request):
    """
    Helper endpoint we built to help the frontend identify who is the current user logged in for that current session
    we'll wrap this in permission handling in the future as well

    Methods:
        GET
    URL:
        /api/authors/current-user
    """
    if request.user and request.user.is_authenticated:
        author = request.user.author_profile
        response = {
            'message': "There is a current user logged in",
            'user': {
                'username': author.username,
                'displayName': author.displayName,
                'author_id': author.id,
            }
        }
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response({'error': "User is not logged in."}, status=status.HTTP_401_UNAUTHORIZED)

def remote_post(request):
    if not request.data.get('comments') or not request.data.get('comments').get('src'):
        return Response({'error': 'No comments object'}, status=status.HTTP_400_BAD_REQUEST)

    for comment in list(request.data.get('comments').get('src')):
        comment['likes'] = comment['likes']['src']

    if not request.data.get('likes') or not request.data.get('likes').get('src'):
        return Response({'error': 'No likes object'}, status=status.HTTP_400_BAD_REQUEST)

    request.data['comments'] = request.data['comments']['src']
    request.data['likes'] = request.data['likes']['src']
    postserializer = RemotePostSerializer(data=request.data)
    if not postserializer.is_valid():
        return Response({'error': postserializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    try:
        Post.objects.get(id_url=request.data.get('id'))
        return Response({'message': 'Post already exists'}, status=status.HTTP_400_BAD_REQUEST)
    except Post.DoesNotExist:
        postserializer.save()

    return Response(postserializer.data, status=status.HTTP_200_OK)

def remote_author(request):
    authorserializer = RemoteAuthorSerializer(data=request.data)
    if not authorserializer.is_valid():
        return Response(authorserializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        Author.objects.get(id_url=request.data['id'])
        return Response({'message': 'Author already exists'}, status=status.HTTP_400_BAD_REQUEST)
    except Author.DoesNotExist:
        authorserializer.save()

    return Response(authorserializer.data, status=status.HTTP_200_OK)

def remote_comment(request):

    if not request.data.get('likes') or not request.data.get('likes').get('src'):
            return Response({'message': 'No likes'}, status=status.HTTP_400_BAD_REQUEST)

    request.data['likes'] = request.data['likes']['src']

    commentserializer = RemoteCommentSerializer(data=request.data)
    if not commentserializer.is_valid():
        return Response(commentserializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        Comment.objects.get(id_url=request.data['id'])
        return Response({'message': 'Comment already exists'}, status=status.HTTP_400_BAD_REQUEST)
    except Comment.DoesNotExist:
        commentserializer.save()

    return Response(commentserializer.data, status=status.HTTP_200_OK)

def remote_like(request):
    likeserializer = RemoteLikeSerializer(data=request.data)
    if not likeserializer.is_valid():
        return Response(likeserializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        author = Author.objects.get(id_url=request.data['author']['id'])
        Like.objects.get(author=author, object=request.data['object'])
        return Response({'message': 'Like already exists'}, status=status.HTTP_400_BAD_REQUEST)
    except (Like.DoesNotExist, Author.DoesNotExist) as e:
        likeserializer.save()

    return Response(likeserializer.data, status=status.HTTP_200_OK)

def remote_follow(request):
    followserializer = RemoteFollowSerializer(data=request.data)
    if not followserializer.is_valid():
        return Response(followserializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        actor_author = Author.objects.get(id_url=request.data['actor']['id'])
        object_author = Author.objects.get(id_url=request.data['object']['id'])
        Follow.objects.get(
            actor=actor_author,
            object=object_author,
        )
        return Response({'message': 'Follow already exists'}, status=status.HTTP_400_BAD_REQUEST)
    except (Follow.DoesNotExist, Author.DoesNotExist) as e:
        followserializer.save()

    return Response(followserializer.data, status=status.HTTP_200_OK)


class Inbox(CreateAPIView):
    def create(self, request, *args, **kwargs):
        if "HTTP_AUTHORIZATION" not in request.META:
            return Response({'error': 'Need to be authenticated to make request to inbox'}, status=status.HTTP_401_UNAUTHORIZED)

        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) != 2 or auth[0].lower() != "basic":
            return Response({'error': 'Need to be authenticated to make request to inbox'}, status=status.HTTP_401_UNAUTHORIZED)

        username, password = b64decode(auth[1]).decode('utf-8').split(':')
        user = authenticate(username=username, password=password)
        if user is not None:
            # TODO: Some sort of validation to check the "user" is a node and not an app "user" since we dont want our users to be able to post to our own inbox
            if request.data['type'] == 'post':
                return remote_post(request)
            elif request.data['type'] == 'author':
                return remote_author(request)
            elif request.data['type'] == 'like':
                return remote_like(request)
            elif request.data['type'] == 'comment':
                return remote_comment(request)
            elif request.data['type'] == 'follow':
                return remote_follow(request)
            else:
                return Response({'error': 'Invalid request type'}, status=status.HTTP_400_BAD_REQUEST)