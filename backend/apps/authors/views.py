from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from .models import Author
from .serializers import AuthorSignUpSerializer, AuthorSerializer
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

class AuthorView(RetrieveAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

    def retrieve(self, request, *args, **kwargs):
        response = super(AuthorView, self).retrieve(request, args, kwargs)
        response.data['type'] = 'author'
        return response
