from django.urls import path
from . import views as authors_views
from ..posts import views as posts_views
from ..follow import views as follows_views

app_name = "authors"
urlpatterns = [
    # Follow app
    # path('/<int:author_id>/inbox',follows_views.FollowView.as_view(),name='follow'),
    path('/<int:author_id>/followers',follows_views.FollowersListView.as_view(),name='followers-list'),
    path('/<int:author_id>/followers/<path:foreign_id_url>',follows_views.FollowerDetailView.as_view(),name='follower-detail'),
    # These three are not required based on spec, but will most likely be used when deciding to display certain posts
    path('/<int:author_id>/following', follows_views.FollowingListView.as_view(),name='following-list'),
    path('/<int:author_id>/following/<path:foreign_id_url>',follows_views.FollowingDetailView.as_view(),name='following-detail'),
    path('/<int:author_id>/friends',follows_views.FriendsListView.as_view(),name='friends-list'),
    path('/<int:author_id>/friends/<path:other_author_url>',follows_views.FriendDetailView.as_view(),name='friend-detail'),

    # Author app
    path('/login', authors_views.AuthorLoginView.as_view(), name='author-login'),
    path('/signup', authors_views.AuthorSignUpView.as_view(), name='author-signup'),
    path('', authors_views.AuthorsView.as_view(), name='authors-list'),
    path('/current-user', authors_views.get_current_user, name='author-current-user'),
    path('/<int:pk>', authors_views.AuthorRetrieveUpdateView.as_view(), name='author-list-or-update'),
    path("/<int:auth_id>/posts/<int:post_id>", posts_views.author_post, name="author-post"),
    path("/<int:auth_id>/posts/", posts_views.PostListCreateView.as_view(), name="author-posts"),
    path('/<path:id_url>', authors_views.get_author_fqid, name='author-list-fqid'),

    # Log In
    path('/current-user', authors_views.get_current_user, name='author-current-user'),

    # Post app
    path("/<int:auth_id>/posts", posts_views.create_post, name="POST Post"),
]