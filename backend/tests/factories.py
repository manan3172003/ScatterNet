import factory
from apps.posts.models import Post
from apps.authors.models import Author
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    password = factory.Faker('password')
    is_staff = factory.Faker('boolean')

# Factory for creating Author instances
class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    user = factory.SubFactory(UserFactory)  # Assuming you want to create a User for each Author
    displayName = factory.Faker('name')
    github = factory.Faker('url')
    profileImageURL = factory.Faker('image_url')
    page = factory.Faker('url')
    is_local = factory.Faker('boolean')
    username = factory.Faker('user_name')
    state = factory.Faker('random_element', elements=['PENDING', 'ACTIVE', 'DELETED'])
    id_url = factory.Faker('url')


# Factory for creating Post instances
class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Faker('sentence', nb_words=6)
    id_url = factory.Faker('url')
    page = factory.Faker('url')
    description = factory.Faker('sentence', nb_words=10)
    contentType = factory.Faker('word')
    content = factory.Faker('paragraph')
    author = factory.SubFactory(AuthorFactory)  # Create an Author instance for the Post
    visibility = factory.Faker('random_element', elements=['PUBLIC', 'FRIENDS', 'UNLISTED', 'DELETED'])
