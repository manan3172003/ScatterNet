from urllib.parse import unquote
from .models import Follow
from ..authors.models import Author
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import FollowSerializer
from django.shortcuts import get_object_or_404

from ..authors.serializers import AuthorSerializer

# Create your views here.
# We may have to move this somewhere else since a few requests use the same URL
class FollowView(APIView):
    def post(self, request, author_id):
        """
        URL: authors/{author_id}/inbox/
        """
        new_request = request.data
        request_type = new_request.get('type')

        if request_type == 'follow':
            actor_id = new_request['actor']['id']
            object_id = new_request['object']['id']

            actor = get_object_or_404(Author, pk=actor_id)
            object = get_object_or_404(Author, pk=object_id)

            new_follow = Follow.objects.create(
                summary=f'{actor.displayName} -> {object.displayName}',
                actor=actor,
                object=object
            )

            return Response({
                'message': 'Follow successfully created',
                'follow': new_follow.summary},
                status=status.HTTP_200_OK)

        return Response({'error': 'Invalid request type'}, status=status.HTTP_400_BAD_REQUEST)

class FollowersListView(APIView):
    """
    URL: authors/{author_id}/followers
    """
    def get(self, request, author_id):
        author = get_object_or_404(Author, pk=author_id)
        authors_followers = Follow.objects.filter(object=author).values_list('actor', flat=True)
        followers = Author.objects.filter(id__in=authors_followers)

        serializer = AuthorSerializer(followers, many=True)
        return Response({
            "type": 'followers',
            "followers": serializer.data,
        }, status=status.HTTP_200_OK)

class FollowerDetailView(APIView):
    """
    URL: authors/{author_id}/followers/{foreign_id_url}/
    """
    def get(self, request, author_id, foreign_id_url):
        decoded_url = unquote(foreign_id_url)
        author = get_object_or_404(Author, pk=author_id)
        foreign_author = get_object_or_404(Author, id_url=decoded_url)

        is_follower = Follow.objects.filter(actor=author, object=foreign_author).exists()
        if not is_follower:
            return Response({"detail": "Not a follower"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"detail": "Is a follower"}, status=status.HTTP_200_OK)

    def delete(self, request, author_id, foreign_id_url):
        decoded_url = unquote(foreign_id_url)
        author = get_object_or_404(Author, pk=author_id)
        foreign_author = get_object_or_404(Author, id_url=decoded_url)

        follow_request = get_object_or_404(Follow, actor=author, object=foreign_author)
        follow_request.delete()

        return Response({
            'message': f'Unfollowed successfully: {follow_request.summary}',
        }, status=status.HTTP_200_OK)

    def put(self, request, author_id, foreign_id_url):
        decoded_url = unquote(foreign_id_url)
        author = get_object_or_404(Author, pk=author_id)
        foreign_author = get_object_or_404(Author, id_url=decoded_url)

        if Follow.objects.filter(actor=author, object=foreign_author).exists():
            return Response(
                {"error": "Follow relationship already exists."},
                status=status.HTTP_409_CONFLICT
            )

        data = {
            "type": "follow",
            "summary": f'{author.displayName} -> {foreign_author.displayName}',
            "actor": author.id,
            "object": foreign_author.id,
        }

        serializer = FollowSerializer(data=data)
        if serializer.is_valid():
            follow_request = serializer.save()
            return Response({
                'message': f'Follow created successfully: {follow_request.summary}',
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FollowingListView(APIView):
    """
    URL: authors/{author_id}/following/
    """
    def get(self, request, author_id):
        author = get_object_or_404(Author, pk=author_id)
        authors_following = Follow.objects.filter(actor=author).values_list('object', flat=True)
        following = Author.objects.filter(id__in=authors_following)

        serializer = AuthorSerializer(following, many=True)
        return Response({
            "type": 'following',
            "following": serializer.data,
        }, status=status.HTTP_200_OK)

class FriendsListView(APIView):
    """
    URL: authors/{author_id}/friends/
    """
    def get(self, request, author_id):
        author = get_object_or_404(Author, pk=author_id)

        authors_following = Follow.objects.filter(actor=author).values_list('object', flat=True)
        authors_followers = Follow.objects.filter(object=author).values_list('actor', flat=True)

        authors_friends = set(authors_following).intersection(authors_followers)

        friends = Author.objects.filter(id__in=authors_friends)

        serializer = AuthorSerializer(friends, many=True)
        return Response({
            "type": 'friends',
            "friends": serializer.data
        }, status=status.HTTP_200_OK)

class FriendDetailView(APIView):
    """
    URL: authors/{author_id}/friends/{other_author_url}/
    """
    def get(self, request, author_id, other_author_url):
        decoded_url = unquote(other_author_url)
        author = get_object_or_404(Author, pk=author_id)
        other_author = get_object_or_404(Author, id_url=decoded_url)

        does_author_follow = Follow.objects.filter(actor=author, object=other_author).exists()
        does_other_author_follow = Follow.objects.filter(object=other_author, actor=author).exists()

        if does_author_follow and does_other_author_follow:
            return Response({
                "relationship": "Are friends"
            }, status=status.HTTP_200_OK)

        else:
            return Response({
                "relationship": "Not friends"
            }, status=status.HTTP_404_NOT_FOUND)