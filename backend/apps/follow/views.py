from urllib.parse import unquote
from .models import Follow
from ..authors.models import Author
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import FollowSerializer, FollowingListSerializer, FriendsListSerializer, FollowersListSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..authors.serializers import AuthorSerializer
from ..utils.helper import send_object


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
    Methods:
        GET

    URL:
        authors/{author_id}/followers
    """

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="List of authors that are followers of the specified author or sent a follow request",
                schema=FollowersListSerializer()
            )
        }
    )
    def get(self, request, author_id):
        """
        This will return a list of authors who are followers of the given author id or a list of authors who sent a follow request.
        """

        isPending = request.GET.get('isPending', "false").lower() == "true"
        author = get_object_or_404(Author, pk=author_id, state="ACTIVE")

        if not isPending:
            authors_followers = Follow.objects.filter(object=author, isPending=False).values_list('actor', flat=True)
            followers = Author.objects.filter(id__in=authors_followers, state="ACTIVE")

            serializer = FollowersListSerializer(instance={
                "type": "followers",
                "followers": followers
            })
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            authors_follow_requests = Follow.objects.filter(object=author, isPending=True).values_list('actor', flat=True)
            follow_requests = Author.objects.filter(id__in=authors_follow_requests, state="ACTIVE")

            serializer = FollowersListSerializer(instance={
                "type": "followers",
                "followers": follow_requests
            })
            return Response(serializer.data, status=status.HTTP_200_OK)

class FollowerDetailView(APIView):
    """
    Methods:
        GET
        DELETE
        PUT

    URL:
        authors/{author_id}/followers/{foreign_id_url}
    """

    def get_permissions(self):
        if self.request.method in ['DELETE', 'PUT']:
            return [IsAuthenticated()]
        return [AllowAny()]

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Returns author details if they are a follower",
                schema=AuthorSerializer()
            ),
            404: openapi.Response(description="Author is not a follower")
        }
    )
    def get(self, request, author_id, foreign_id_url):
        """
        Handles a GET request that would return foreign author's details if they are a follower
        """

        decoded_url = unquote(foreign_id_url)
        author = get_object_or_404(Author, pk=author_id, state='ACTIVE')
        foreign_author = get_object_or_404(Author, id_url=decoded_url, state='ACTIVE')

        is_follower = Follow.objects.filter(actor=foreign_author, object=author, isPending=False).exists()
        follower_data = AuthorSerializer(foreign_author).data

        if not is_follower:
            return Response({"error": "Not a follower"}, status=status.HTTP_404_NOT_FOUND)
        return Response(follower_data, status=status.HTTP_200_OK)

    """
    ://service/api/authors/{AUTHOR_1_SERIAL}/followers/{AUTHOR_2_SERIAL}
    if AUTHOR_2 is logged in and makes PUT request:
        - if there is no request:
            - AUTHOR_2 makes the follow request to author 1
        - if there is a request:
            - error: Follow request already sent
 
    if AUTHOR_1 is logged in and makes PUT request:
        - if there is a request:
            - AUTHOR_1 makes the PUT request to accept the follow request
        - if there is no request:
            - Error
    """

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description="Follow request accepted"),
            201: openapi.Response(description="Follow request successfully created"),
            400: openapi.Response(description="Follow request already sent"),
            409: openapi.Response(description="Follow relationship already exists and is accepted"),
        }
    )
    def put(self, request, author_id, foreign_id_url):
        """
            Handles PUT requests that would send or accept a follow request.
        """

        decoded_url = unquote(foreign_id_url)
        author = get_object_or_404(Author, pk=author_id, state="ACTIVE")
        foreign_author = get_object_or_404(Author, id_url=decoded_url, state="ACTIVE")

        if foreign_author.id == author.id:
            return Response({
                'error': 'Actor and object cannot be the same user'
            }, status=status.HTTP_401_UNAUTHORIZED)

        existing_follow = Follow.objects.filter(actor=foreign_author, object=author).first()

        # Check if follow exists
        # If isPending -> accept, if not, send an errpr
        if existing_follow:

            # Ensure the person accepting the friend request is the author
            if request.user.author_profile.id != author.id:
                return Response({
                    'error': 'Follow request has already been sent'
                }, status=status.HTTP_400_BAD_REQUEST)

            if existing_follow.isPending:
                existing_follow.isPending = False
                existing_follow.save()
                return Response({"message": "Follow request accepted"}, status=status.HTTP_200_OK)

            else:
                return Response({
                    "error": "Follow relationship already exists and is accepted"
                }, status=status.HTTP_409_CONFLICT)

        # Ensure the person making the follow request is the foreign_author
        if request.user.author_profile.id != foreign_author.id:
            return Response({
                'error': 'Need to be logged in as the follow requester to perform this action'
            }, status=status.HTTP_401_UNAUTHORIZED)

        data = {
            "actor": foreign_author.id,
            "object": author.id,
        }

        serializer = FollowSerializer(data=data)
        if serializer.is_valid():
            follow_request = serializer.save() #we assume that its a local author

            #for a non local author we assume that we have already started following them
            if not author.is_local:
                built_follow_request = Follow.objects.get(actor=foreign_author, object=author)
                built_follow_request.isPending = False
                built_follow_request.save()
                follow_request_dict = serializer.data
                follow_request_dict['actor'] = AuthorSerializer(Author.objects.get(id=follow_request_dict.get('actor'))).data
                follow_request_dict['object'] = AuthorSerializer(Author.objects.get(id=follow_request_dict.get('object'))).data
                send_object(follow_request_dict, [author])

            return Response({
                'message': 'Follow request successfully created',
                'follow': f"{follow_request.actor.displayName} -> {follow_request.object.displayName}"
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    """
    if AUTHOR_1 follow requests AUTHOR_2:
        - if AUTHOR_1 is logged in:
            - Cannot delete
        - if AUTHOR_2 is logged in:
            - Successful delete
    
    if AUTHOR_1 follows AUTHOR_2:
        - if AUTHOR_1 is logged in:
            - Successful Unfollow
        - if AUTHOR_2 is logged in:
            - Cannot delete
    """

    @swagger_auto_schema(
        responses={
            200: openapi.Response(description="Follow request rejected / Unfollowed successfully"),
            401: openapi.Response(description="Unauthorized: Must be logged in as the correct user"),
        }
    )
    def delete(self, request, author_id, foreign_id_url):
        """
        Handles rejecting a follow request or unfollowing an author.
        """

        decoded_url = unquote(foreign_id_url)
        author = get_object_or_404(Author, pk=author_id, state="ACTIVE")
        foreign_author = get_object_or_404(Author, id_url=decoded_url, state="ACTIVE")

        follow_request = get_object_or_404(Follow, actor=foreign_author, object=author)


        # When rejecting the follow request, the user logged in has to be the author
        # that is receiving the follow request (FOREIGN_AUTHOR_FQID -> AUTHOR_SERIAL)
        if follow_request.isPending:
            if request.user.author_profile.id != author.id:
                return Response({
                    'error': 'Need to be logged in as the follow requestee to perform this action'
                }, status=status.HTTP_401_UNAUTHORIZED)

            follow_request.delete()
            return Response({
                'message': 'Follow request rejected'
            }, status=status.HTTP_200_OK)

        # When unfollowing someone, the user logged in has to be the author
        # that made the request, which would be the foreign_author_fqid
        if request.user.author_profile.id != foreign_author.id:
            return Response({
                'error': 'Need to be logged in as the follower to perform this action'
            }, status=status.HTTP_401_UNAUTHORIZED)

        follow_request.delete()
        return Response({
            'message': 'Unfollowed successfully',
        }, status=status.HTTP_200_OK)

class FollowingListView(APIView):
    """
    Methods:
        GET

    URL:
        authors/{author_id}/following/
    """

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="List of authors that the specified author is following or sent a follow request to",
                schema=FollowingListSerializer()
            )
        }
    )
    def get(self, request, author_id):
        """
        This will return a list of authors who the author follows or sent a follow request to.
        """

        isPending = request.GET.get('isPending', "false").lower() == "true"
        author = get_object_or_404(Author, pk=author_id, state='ACTIVE')

        if not isPending:
            authors_following = Follow.objects.filter(actor=author, isPending=False).values_list('object', flat=True)
            following = Author.objects.filter(id__in=authors_following, state='ACTIVE')

            serializer = FollowingListSerializer(instance={
                "type": "following",
                "following": following
            })
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            authors_following_requests = Follow.objects.filter(actor=author, isPending=True).values_list('object', flat=True)
            following_requests = Author.objects.filter(id__in=authors_following_requests, state='ACTIVE')

            serializer = FollowingListSerializer(instance={
                "type": "following",
                "following": following_requests
            })
            return Response(serializer.data, status=status.HTTP_200_OK)

class FollowingDetailView(APIView):
    """
    Methods:
        GET

    URL:
        authors/{author_id}/following/{foreign_id_url}
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Returns author details if the author is following the author specified in the foreign id",
                schema=AuthorSerializer()
            ),
            404: openapi.Response(description="Author is not following the other author"),
        }
    )
    def get(self, request, author_id, foreign_id_url):
        """
        Handles a GET request that would return foreign author's details if they are followed by the author
        """
        decoded_url = unquote(foreign_id_url)
        author = get_object_or_404(Author, pk=author_id, state='ACTIVE')
        foreign_author = get_object_or_404(Author, id_url=decoded_url, state='ACTIVE')

        is_following = Follow.objects.filter(actor=author, object=foreign_author, isPending=False).exists()
        following_data = AuthorSerializer(foreign_author).data

        if not is_following:
            return Response({"error": "Not following"}, status=status.HTTP_404_NOT_FOUND)
        return Response(following_data, status=status.HTTP_200_OK)

class FriendsListView(APIView):
    """
    METHODS:
        GET

    URL:
        authors/{author_id}/friends/
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="List of authors that the specified author are friends with",
                schema=FriendsListSerializer()
            )
        }
    )
    def get(self, request, author_id):
        """
        Returns a list of authors that the specified author are friends with.
        """
        author = get_object_or_404(Author, pk=author_id, state='ACTIVE')

        authors_following = Follow.objects.filter(actor=author, isPending=False).values_list('object', flat=True)
        authors_followers = Follow.objects.filter(object=author, isPending=False).values_list('actor', flat=True)
        authors_friends = set(authors_following).intersection(authors_followers)

        friends = Author.objects.filter(id__in=authors_friends)

        serializer = FriendsListSerializer(instance={
            "type": "following",
            "friends": friends
        })
        return Response(serializer.data, status=status.HTTP_200_OK)

class FriendDetailView(APIView):
    """
    Methods:
        GET

    URL:
        authors/{author_id}/friends/{other_author_url}/
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Returns author details if the two authors are friends",
                schema=AuthorSerializer()
            ),
            404: openapi.Response(description="The two authors are not friends")
        }
    )
    def get(self, request, author_id, other_author_url):
        """
        Returns author details if the two authors are friends.
        """
        decoded_url = unquote(other_author_url)
        author = get_object_or_404(Author, pk=author_id, state='ACTIVE')
        other_author = get_object_or_404(Author, id_url=decoded_url, state='ACTIVE')

        does_author_follow = Follow.objects.filter(actor=author, object=other_author, isPending=False).exists()
        does_other_author_follow = Follow.objects.filter(object=other_author, actor=author, isPending=False).exists()

        if does_author_follow and does_other_author_follow:
            friend_data = AuthorSerializer(author).data
            return Response(friend_data, status=status.HTTP_200_OK)

        else:
            return Response({"error": "Not friends"}, status=status.HTTP_404_NOT_FOUND)