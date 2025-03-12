from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.apps import apps
from django.db import connection
from ....authors.models import Author  # Replace with your actual app name
from ....follow.models import Follow
from ....posts.models import Post, Comment, Like

class Command(BaseCommand):
    help = 'Add initial user and author data to the database'
    def handle(self, *args, **kwargs):

        # Create Users
        admin_user = User.objects.create_user(
            username='admin',
            password='admin',
            is_active=True,
            is_staff=True,
        )

        user1_user = User.objects.create_user(
            username='johndoe',
            password='johndoe',
            is_active=True,
            is_staff=False,
        )

        user2_user = User.objects.create_user(
            username='janedoe',
            password='janedoe',
            is_active=True,
            is_staff=False,
        )

        user3_user = User.objects.create_user(
            username='jacob',
            password='jacob',
            is_active=True,
            is_staff=False,
        )

        # Create Authors
        admin_author = Author.objects.create(
            user=admin_user,
            displayName='admin',
            github='',
            profileImageURL='',
            page='',
            is_local=True,
            username='admin',
            state='ACTIVE',
            id_url='http://localhost:8000/api/authors/1',
        )

        user1_author = Author.objects.create(
            user=user1_user,
            displayName='John Doe',
            github='',
            profileImageURL='',
            page='',
            is_local=True,
            username='johndoe',
            state='ACTIVE',
            id_url='http://localhost:8000/api/authors/2'
        )

        user2_author = Author.objects.create(
            user=user2_user,
            displayName='Jane Doe',
            github='',
            profileImageURL='',
            page='',
            is_local=True,
            username='janedoe',
            state='ACTIVE',
            id_url='http://localhost:8000/api/authors/3'
        )

        user3_author = Author.objects.create(
            user=user3_user,
            displayName='Jacob',
            github='',
            profileImageURL='',
            page='',
            is_local=True,
            username='jacob',
            state='ACTIVE',
            id_url='http://localhost:8000/api/authors/4'
        )

        # Create follow relations

        # John doe follows Jane doe
        Follow.objects.create(
            actor=user1_author,
            object=user2_author,
            isPending=False
        )

        # Jane doe follows John doe
        Follow.objects.create(
            actor=user2_author,
            object=user1_author,
            isPending=False
        )

        # Jacob follow requested John doe
        Follow.objects.create(
            actor=user3_author,
            object=user1_author,
            isPending=True
        )

        # John doe follows Jacob
        Follow.objects.create(
            actor=user1_author,
            object=user3_author,
            isPending=False
        )

        # Jane doe follow requested Jacob
        Follow.objects.create(
            actor=user2_author,
            object=user3_author,
            isPending=True
        )

        # Create Posts


        self.stdout.write(self.style.SUCCESS('Successfully added users and authors'))