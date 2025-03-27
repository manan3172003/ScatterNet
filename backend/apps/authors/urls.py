from django.urls import path
from . import views as authors_views
from ..posts import views as posts_views
from ..follow import views as follows_views

app_name = "authors"
urlpatterns = [
    # Author fixed endpoints
    path('/login', authors_views.AuthorLoginView.as_view(), name='author-login'),
    path('/logout', authors_views.AuthorLogoutView.as_view(), name='author-logout'),
    path('/signup', authors_views.AuthorSignUpView.as_view(), name='author-signup'),
    path('/current-user', authors_views.get_current_user, name='author-current-user'),
    path('', authors_views.AuthorsView.as_view(), name='authors-list'),
    path('/<int:pk>', authors_views.AuthorRetrieveUpdateView.as_view(), name='author-list-or-update'),

    # Follow app endpoints numeric converter first, more specific before less specific
    path('/<int:author_id>/followers/<path:foreign_id_url>', follows_views.FollowerDetailView.as_view(), name='follower-detail'),
    path('/<int:author_id>/followers', follows_views.FollowersListView.as_view(), name='followers-list'),
    path('/<int:author_id>/friends/<path:other_author_url>', follows_views.FriendDetailView.as_view(), name='friend-detail'),
    path('/<int:author_id>/friends', follows_views.FriendsListView.as_view(), name='friends-list'),
    path('/<int:author_id>/following', follows_views.FollowingListView.as_view(), name='following-list'),
    path('/<int:author_id>/following/<path:foreign_id_url>',follows_views.FollowingDetailView.as_view(),name='following-detail'),

    # Likes endpoints with numeric converters
    path("/<int:author_serial>/posts/<int:post_serial>/comments/<path:comment_fqid>/likes", posts_views.LikesListView.as_view(), name="author-post-comment-likes"),
    path("/<int:author_serial>/liked/<int:like_serial>", posts_views.LikeRetrieveView.as_view(), name="author-single-liked"),
    path("/<int:author_serial>/commented/<int:comment_serial>", posts_views.CommentRetrieveView.as_view(), name="author-single-comment"),
    path("/<int:author_serial>/posts/<int:post_serial>/likes", posts_views.LikesListView.as_view(), name="author-post-likes"),
    path("/<int:author_serial>/posts/<int:post_serial>/comments", posts_views.CommentsListView.as_view(), name="author-post-comments"),
    path("/<int:author_serial>/posts/<int:post_serial>/image", posts_views.ImagePostsView.as_view(), name="author-post-image"),
    path("/<int:author_serial>/liked", posts_views.LikesListView.as_view(), name="author-liked"),
    path("/<int:author_serial>/commented", posts_views.CommentedListCreateView.as_view(), name="author-commented"),


    # Post app endpoints
    path("/<int:auth_id>/posts/<int:post_id>", posts_views.author_post, name="author-post"),
    path("/<int:auth_id>/posts", posts_views.PostListCreateView.as_view(), name="author-posts"),

    # Likes endpoints with a generic path converter

    path("/<path:author_fqid>/liked", posts_views.LikesListView.as_view(), name="author-id_url-liked"),
    path("/<path:author_fqid>/commented", posts_views.CommentedListCreateView.as_view(), name="author-id_url-commented"),
    path("/<path:author_fqid>/inbox", authors_views.AuthorInbox.as_view(), name="author-inbox"),

    path('/<path:id_url>', authors_views.get_author_fqid, name='author-list-fqid'),
]
