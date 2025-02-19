from urllib.parse import unquote

from django.http.response import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
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

# @api_view(["GET", "POST"])
# def get_posts(request):
#     posts = Post.objects.all()
#     serializer = PostSerializer(posts, many=True)
#     return Response(serializer.data)

class PostListCreateView(APIView, ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostsPaginator

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            queryset = Post.objects.filter(author_id=kwargs.get("auth_id"),visibility='PUBLIC').values()
        elif request.user.author_profile





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