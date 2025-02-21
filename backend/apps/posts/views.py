from urllib.parse import unquote

from django.http.response import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from rest_framework.generics import ListAPIView
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

# def get_author_post(auth_id, post_id):
#     post =
# def put_author_post(request, auth_id, post_id):
# def delete_author_post(request, auth_id, post_id):
#
# @api_view(["GET", "PUT", "DELETE"])
# def author_post(request, auth_id, post_id):
#     if request.method == 'GET':
#         get_author_post(auth_id, post_id)
#     elif request.method == 'PUT':
#         put_author_post(request, auth_id, post_id)
#     elif request.method == 'DELETE':
#         delete_author_post(request, auth_id, post_id)

@api_view(["GET"])
def get_posts(request):
    try:
        posts = Post.objects.all()
    except Post.DoesNotExist:
        return Response({})
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

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

@api_view(["POST"])
def create_post(request, auth_id):
    data = request.data
    data["author_id"] = auth_id
    serializer = PostSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

"""
{
"title": "new post",
"description": "new description",
"contentType": "text",
"content": "my post content"
}
"""