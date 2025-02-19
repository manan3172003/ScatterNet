from django.urls import path
from . import views

app_name = "authors"
urlpatterns = [
    path('/login', views.AuthorLoginView.as_view(), name='author-login'),
    path('/signup', views.AuthorSignUpView.as_view(), name='author-signup'),
    path('', views.AuthorsView.as_view(), name='authors-list'),
    path('/<int:pk>', views.AuthorRetrieveUpdateView.as_view(), name='author-list-or-update'),
]