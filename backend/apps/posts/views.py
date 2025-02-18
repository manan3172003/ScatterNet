from urllib.parse import unquote

from django.http.response import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer


# Create your views here.
@api_view(["GET"])
def get_post(request, url_id):
    decoded_url = unquote(url_id)
    try:
        post = Post.objects.get(id_url=decoded_url)
        if post.visibility != 'PUBLIC':
            raise Http404
    except Post.DoesNotExist:
        raise Http404
    serializer = PostSerializer(post)
    return Response(serializer.data)

@api_view(["GET"])
def get_posts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

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