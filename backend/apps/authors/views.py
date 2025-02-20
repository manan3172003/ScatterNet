from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from urllib.parse import unquote
from .models import Author
from .serializers import AuthorSignUpSerializer, AuthorSerializer, AuthorUpdateSerializer
from ..utils.paginators import AuthorsPaginator

# Create your views here.
class AuthorLoginView(APIView):
    """
    This will be the path handling all login work
    We'll take the info from the frontend and authenticate a user n use django sessions
    to sustain it
    """

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        return Response({'detail': 'CSRF cookie set.'})

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

class AuthorSignUpView(APIView):
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
    serializer_class = AuthorSerializer
    pagination_class = AuthorsPaginator
    def get_queryset(self):
        state = self.request.query_params.get('state')
        if state:
            queryset = Author.objects.filter(state=state)
        else:
            queryset = Author.objects.all()

        username = self.request.query_params.get('username')
        host = self.request.query_params.get('host')

        if username:
            queryset = queryset.filter(username=username)
        if host:
            queryset = queryset.filter(host=host)

        return queryset

class CheckNodeAdminChangedState(BasePermission):

    # https://www.django-rest-framework.org/api-guide/permissions/#custom-permissions neat feature
    message = "Only Node Admins are Allowed to update an Author's state."

    def has_permission(self, request, view):
        if request.method == 'PUT' and 'state' in request.data:
            return request.user.is_authenticated and request.user.is_staff
        return True

class AuthorRetrieveUpdateView(RetrieveUpdateAPIView):
    queryset = Author.objects.all()
    http_method_names = ['get', 'put'] #explicitly only allows these two
    permission_classes = [CheckNodeAdminChangedState]

    def retrieve(self, request, *args, **kwargs):
        response = super(AuthorRetrieveUpdateView, self).retrieve(request, args, kwargs)
        # response.data['type'] = 'author'
        return response

    #since we need the same endpoint, just change serializer being used based on what task we're doing
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AuthorSerializer
        else:
            return AuthorUpdateSerializer

@api_view(['GET'])
def get_author_fqid(request, id_url):
    decoded_url = unquote(id_url)
    try:
        author = Author.objects.get(id_url=decoded_url)
    except Author.DoesNotExist:
        return Response({'error': 'Author does not exist with this id'}, status=status.HTTP_404_NOT_FOUND)
    serializer = AuthorSerializer(author)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_current_user(request):
    if request.user.is_authenticated:
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


