from django.urls import path
from . import views

app_name = "authors"
urlpatterns = [
    path('/login', views.AuthorLoginView.as_view(), name='author-login'),
    path('/signup', views.AuthorSignUpView.as_view(), name='author-signup'),
    path('', views.AuthorsView.as_view(), name='authors-list'),
    path('/<int:pk>', views.AuthorRetrieveUpdateView.as_view(), name='author-list-or-update'),
    path('/<path:id_url>', views.get_author_fqid, name='author-list-fqid'),
    path('/current-user', views.get_current_user, name='author-current-user')
]