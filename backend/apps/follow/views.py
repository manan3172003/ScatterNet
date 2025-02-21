from urllib.parse import unquote
from .models import Follow
from ..authors.models import Author
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import FollowSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from ..authors.serializers import AuthorSerializer

# Create your views here.
# We may have to move this somewhere else since a few requests use the same URL
# class FollowView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, author_id):
#         """
#         URL: authors/{author_id}/inbox
#         """
#         new_request = request.data
#         request_type = new_request.get('type')
#
#         if request_type != 'follow':
#             return Response({'error': 'Invalid request type'}, status=status.HTTP_400_BAD_REQUEST)
#
#         actor_id = new_request['actor']['id']
#         object_id = new_request['object']['id']
#
#         actor = get_object_or_404(Author, id_url=actor_id)
#         object = get_object_or_404(Author, id_url=object_id)
#
#         # Ensure logged-in user is the actor
#         if request.user.author_profile.id != actor.id:
#             return Response({
#                 'error': 'You need to be the actor.'
#             }, status=status.HTTP_401_UNAUTHORIZED)
#
#         # Ensure author and object aren't the same
#         if request.user.author_profile.id == object.id:
#             return Response({
#                 'error': 'Actor and object cannot be the same user.'
#             }, status=status.HTTP_401_UNAUTHORIZED)
#
#         # Check if follow relationship already exists
#         if Follow.objects.filter(actor=actor, object=object).exists():
#             return Response({
#                 'error': 'Follow relationship already exists.'
#             }, status=status.HTTP_409_CONFLICT)
#
#         data = {
#             'actor': actor.id,
#             'object': object.id,
#         }
#
#         serializer = FollowSerializer(data=data)
#         if serializer.is_valid():
#             follow = serializer.save()
#             return Response({
#                 'message': 'Follow successfully created',
#                 'follow': f"{follow.actor.displayName} -> {follow.object.displayName}"
#             }, status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FollowersListView(APIView):
    """
    URL: authors/{author_id}/followers
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, author_id):
        author = get_object_or_404(Author, pk=author_id, state="ACTIVE")
        authors_followers = Follow.objects.filter(object=author).values_list('actor', flat=True)
        followers = Author.objects.filter(id__in=authors_followers, state="ACTIVE")

        serializer = AuthorSerializer(followers, many=True)
        return Response({
            "type": 'followers',
            "followers": serializer.data,
        }, status=status.HTTP_200_OK)

class FollowerDetailView(APIView):
    """
    URL: authors/{author_id}/followers/{foreign_id_url}
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, author_id, foreign_id_url):
        decoded_url = unquote(foreign_id_url)
        author = get_object_or_404(Author, pk=author_id, state='ACTIVE')
        foreign_author = get_object_or_404(Author, id_url=decoded_url, state='ACTIVE')

        is_follower = Follow.objects.filter(actor=author, object=foreign_author).exists()

        # Could change if we need more info
        if not is_follower:
            return Response({"relationship": "Not a follower"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"relationship": "Is a follower"}, status=status.HTTP_200_OK)

    def delete(self, request, author_id, foreign_id_url):
        decoded_url = unquote(foreign_id_url)
        author = get_object_or_404(Author, pk=author_id, state="ACTIVE")
        foreign_author = get_object_or_404(Author, id_url=decoded_url, state="ACTIVE")

        if request.user.author_profile.id != author.id:
            return Response({
                'error': 'Need to be logged in as the author'
            }, status=status.HTTP_401_UNAUTHORIZED)

        follow_request = get_object_or_404(Follow, actor=author, object=foreign_author)
        follow_request.delete()

        return Response({
            'message': 'Unfollowed successfully',
        }, status=status.HTTP_200_OK)

    def put(self, request, author_id, foreign_id_url):
        decoded_url = unquote(foreign_id_url)
        author = get_object_or_404(Author, pk=author_id, state="ACTIVE")
        foreign_author = get_object_or_404(Author, id_url=decoded_url, state="ACTIVE")

        if request.user.author_profile.id != author.id:
            return Response({
                'error': 'Need to be logged in as the user to perform this action'
            }, status=status.HTTP_401_UNAUTHORIZED)

        if Follow.objects.filter(actor=author, object=foreign_author).exists():
            return Response({
                "error": "Follow relationship already exists."
            }, status=status.HTTP_409_CONFLICT)

        if request.user.author_profile.id == foreign_author.id:
            return Response({
                'error': 'Actor and object cannot be the same user'
            }, status=status.HTTP_401_UNAUTHORIZED)

        data = {
            "actor": author.id,
            "object": foreign_author.id,
        }

        serializer = FollowSerializer(data=data)
        if serializer.is_valid():
            follow_request = serializer.save()
            return Response({
                'message': 'Follow successfully created',
                'follow': f"{follow_request.actor.displayName} -> {follow_request.object.displayName}"
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FollowingListView(APIView):
    """
    URL: authors/{author_id}/following/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, author_id):
        author = get_object_or_404(Author, pk=author_id, state='ACTIVE')
        authors_following = Follow.objects.filter(actor=author).values_list('object', flat=True)
        following = Author.objects.filter(id__in=authors_following, state='ACTIVE')

        serializer = AuthorSerializer(following, many=True)
        return Response({
            "type": 'following',
            "following": serializer.data,
        }, status=status.HTTP_200_OK)

class FriendsListView(APIView):
    """
    URL: authors/{author_id}/friends/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, author_id):
        author = get_object_or_404(Author, pk=author_id, state='ACTIVE')

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
    permission_classes = [IsAuthenticated]

    def get(self, request, author_id, other_author_url):
        decoded_url = unquote(other_author_url)
        author = get_object_or_404(Author, pk=author_id, state='ACTIVE')
        other_author = get_object_or_404(Author, id_url=decoded_url, state='ACTIVE')

        does_author_follow = Follow.objects.filter(actor=author, object=other_author).exists()
        does_other_author_follow = Follow.objects.filter(object=other_author, actor=author).exists()

        if does_author_follow and does_other_author_follow:
            return Response({"relationship": "Are friends"}, status=status.HTTP_200_OK)

        else:
            return Response({"relationship": "Not friends"}, status=status.HTTP_404_NOT_FOUND)