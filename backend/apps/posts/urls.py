from django.urls import path
from . import views

app_name = "posts"
urlpatterns = [
    # use encoded url for url_id
    path("/<path:url_id>/", views.get_post, name="GET Post"),
    path("/<path:post_fqid>/likes", views.LikesListView.as_view(), name="post-likes"),
]
