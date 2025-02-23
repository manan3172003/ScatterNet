from django.urls import path
from . import views

app_name = "posts"
urlpatterns = [
    # use encoded url for url_id
    path("/<path:url_id>", views.get_post, name="GET Post"),
    path("/<path:post_fqid>/comments", views.CommentsListView.as_view(), name="post-comments"),
    path("/<path:post_fqid>/likes", views.LikesListView.as_view(), name="post-likes"),
    path("", views.StreamListView.as_view(), name="stream-list"),
]
