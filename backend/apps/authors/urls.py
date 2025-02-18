from django.urls import path
from . import views

app_name = "authors"
urlpatterns = [
    path('api/author/login', views.AuthorLoginView.as_view(), name='author-login')
]