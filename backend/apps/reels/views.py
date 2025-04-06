from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db.models import F, Q
from django.db import models
from apps.authors.models import Author
from django.http import HttpResponse, StreamingHttpResponse
import os
import re
from apps.follow.models import Follow
import mimetypes

from .models import Reel, ReelComment, ReelLike, ReelCommentLike
from .serializers import (
    ReelSerializer, 
    ReelCommentSerializer, 
    ReelLikeSerializer,
    ReelCommentLikeSerializer
)

def ranged_file_response(file_path, request, content_type):
    """
    Serve a file with proper support for HTTP range requests.
    This enables video seeking in browsers.
    Args:
        file_path: The path to the file on disk
        request: The HTTP request object
        content_type: The MIME type of the file
    Returns:
        An HttpResponse or StreamingHttpResponse object with appropriate headers
    """
    file_size = os.path.getsize(file_path)
    
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_match = re.match(r'bytes=(\d+)-(\d*)', range_header)
    if range_match:
        start = int(range_match.group(1))
        end = int(range_match.group(2)) if range_match.group(2) else file_size - 1
        
        # Ensuring the requested range is valid
        if start >= file_size:
            # Return 416 Range Not Satisfiable if the range is invalid https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/416
            response = HttpResponse(status=416)
            response['Content-Range'] = f'bytes */{file_size}'
            return response
        
        if end >= file_size:
            end = file_size - 1
        
        content_length = end - start + 1
        
        # Creating streaming response with appropriate headers. Streaming file in chunks
        response = StreamingHttpResponse(
            streaming_content=ranged_file_iterator(file_path, start, end),
            status=206,  # 206 Partial Content status code
            content_type=content_type
        )
        response['Content-Length'] = str(content_length)
        response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
        response['Accept-Ranges'] = 'bytes' 
        response['Cache-Control'] = 'public, max-age=3600'
        
        return response
    else:
        # No Range header was present, so we serve the full file
        response = HttpResponse(open(file_path, 'rb'), content_type=content_type)
        response['Content-Length'] = str(file_size)
        response['Accept-Ranges'] = 'bytes' 
        response['Cache-Control'] = 'public, max-age=3600'        
        return response

def ranged_file_iterator(file_path, start, end, chunk_size=8192):
    """
    Generator to stream file in chunks with proper range support.
    Used in the stream endpoint.
    
    Args:
        file_path: Path to the file
        start: Starting byte position (inclusive)
        end: Ending byte position (inclusive)
        chunk_size: Size of chunks to yield
    """
    with open(file_path, 'rb') as f:
        f.seek(start)  # Move file pointer to the requested start position
        remaining = end - start + 1
        while remaining > 0:
            chunk = f.read(min(chunk_size, remaining))
            if not chunk:  # End of file so break while
                break
            remaining -= len(chunk)
            yield chunk 

class ReelViewSet(viewsets.ModelViewSet):
    """
    API endpoint for reels 
    """
    queryset = Reel.objects.all()
    serializer_class = ReelSerializer
    
    def get_queryset(self):
        """
        Override to apply visibility filtering for all ViewSet methods
        This ensures the list, retrieve, and other methods all follow the same visibility rules for unlisted, public and friends only
        """
        queryset = Reel.objects.all()
        
        is_detail_view = self.kwargs.get('pk') is not None
        
      
        if self.request.user.is_authenticated:
            try:
                author = self.request.user.author_profile
                
                # List of authors user follows
                following = Follow.objects.filter(actor=author, isPending=False).values_list('object_id', flat=True)
                
                if is_detail_view:
                    queryset = queryset.filter(
                        # Show all public reels
                        models.Q(visibility='PUBLIC') |
                        # Show all unlisted reels (anyone with link)
                        models.Q(visibility='UNLISTED') |
                        # Show user's own reels
                        models.Q(author=author) |
                        # Show FRIENDS reels only from people the user follows
                        (models.Q(visibility='FRIENDS') & models.Q(author_id__in=following))
                    )
                else:
                    queryset = queryset.filter(
                     
                        models.Q(visibility='PUBLIC') |
                        models.Q(author=author) |
                        (models.Q(visibility='FRIENDS') & models.Q(author_id__in=following)) |
                        (models.Q(visibility='UNLISTED') & models.Q(author_id__in=following))
                    )
            except AttributeError:
                # User not logged in/no profile
                if is_detail_view:
                    queryset = queryset.filter(
                        models.Q(visibility='PUBLIC') | 
                        models.Q(visibility='UNLISTED')
                    )
                else:
                    queryset = queryset.filter(visibility='PUBLIC')
        else:
            # Unauth can still see public and unlisted posts
            if is_detail_view:
                queryset = queryset.filter(
                    models.Q(visibility='PUBLIC') | 
                    models.Q(visibility='UNLISTED')
                )
            else:
                queryset = queryset.filter(visibility='PUBLIC')
            
        return queryset
    
    def perform_create(self, serializer):  
        try:
            author = self.request.user.author_profile
        except AttributeError:
            author = Author.objects.get(user=self.request.user)
            
        serializer.save(author=author)
    
    def create(self, request, *args, **kwargs):
        """Create a new reel with the uploaded video."""
        try:
            author = request.user.author_profile
            
            if 'video' not in request.FILES:
                return Response(
                    {'error': 'No video file provided'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            video_file = request.FILES['video']
            visibility = request.data.get('visibility', 'PUBLIC')
            
            if visibility not in dict(Reel.VISIBILITY_CHOICES):
                visibility = 'PUBLIC'
            
            reel = Reel.objects.create(
                author=author,
                video=video_file,
                caption=request.data.get('caption',""),
                visibility=visibility,
                duration=0.0  
            )
            
            serializer = self.get_serializer(reel)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Like a reel"""
        try:
            # Validate user is authenticated
            if not request.user.is_authenticated:
                return Response(
                    {'detail': 'Authentication required'},
                    status=status.HTTP_401_UNAUTHORIZED # Can only like stuff is authenitciated
                )
            
            # get_object() uses get_queryset() which applies our visibility filters
    
            reel = self.get_object()
            author = request.user.author_profile
            
            # Check if already liked
            if ReelLike.objects.filter(reel=reel, author=author).exists():
                return Response(
                    {'detail': 'You have already liked this reel.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            like = ReelLike.objects.create(reel=reel, author=author)
            
            return Response(
                ReelLikeSerializer(like).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """Get comments for a reel"""
        # get_object() uses get_queryset() which applies our visibility filters
        reel = self.get_object()
        
        # get_queryset() has already verified visibility permissions
        comments = ReelComment.objects.filter(reel=reel)
        
        serializer = ReelCommentSerializer(
            comments, 
            many=True, 
            context={'request': request}
        )
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        """Add a comment to a reel"""
        try:
            # Validate user is authenticated
            if not request.user.is_authenticated:
                return Response(
                    {'detail': 'Authentication required'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            reel = self.get_object()
            author = request.user.author_profile
            
            # get_queryset() has already verified permissions so we can go straight to making the comment
            
            # Get the comment content
            content = request.data.get('content')
            contentType = request.data.get('contentType', 'text/plain')
            if not content:
                return Response(
                    {'detail': 'Comment content is required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            comment = ReelComment.objects.create(
                reel=reel, 
                author=author, 
                content=content,
                contentType=contentType
            )
        
            
            # Serialize for response
            serializer = ReelCommentSerializer(comment, context={'request': request})
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        
       
        except Exception as e:
            # Catch any other exceptions
            print(f"Error creating comment: {str(e)}")
            return Response(
                {'detail': f'Error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    
    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        """Unlike a reel"""
        try:
            if not request.user.is_authenticated:
                return Response(
                    {'detail': 'Authentication required'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            reel = self.get_object()
            author = request.user.author_profile
            like = ReelLike.objects.filter(reel=reel, author=author).first()
            if not like:
                return Response(
                    {'detail': 'You have not liked this reel.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            like.delete()
            
            return Response(
                {'detail': 'Like removed successfully.'},
                status=status.HTTP_200_OK
            )
        
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def view(self, request, pk=None):
        """Increment view count for a reel"""
        reel = self.get_object()
        reel.view_count = F('view_count') + 1
        reel.save()
        reel.refresh_from_db()
        
        return Response({
            'view_count': reel.view_count
        })
        
    @action(detail=True, methods=['get'])
    def stream(self, request, pk=None):
        """
        Endpoint that streams a video file with proper HTTP range request support.
        Video seeking achieved by handling HTTP Range headers.
        
        Returns:
            StreamingHttpResponse: A streaming response containing the requested video portion
        """
        try:
            reel = self.get_object()
            
            # UNLISTED reels are accessible to anyone with the link
            if reel.visibility == 'FRIENDS':
                # Verify user is authenticated
                if not request.user.is_authenticated:
                    return Response(
                        {'error': 'This video requires authentication to view'},
                        status=status.HTTP_401_UNAUTHORIZED
                    )
            
                try:
                    author = request.user.author_profile
                    if author == reel.author:
                        # Author can see their own content
                        pass
                    else:
                        is_following = Follow.objects.filter(actor=author, object=reel.author, isPending=False).exists()
                        
                        if not is_following:
                            return Response(
                                {'error': 'You must follow the creator to view this video'},
                                status=status.HTTP_403_FORBIDDEN
                            )
                except AttributeError:
                    return Response(
                        {'error': 'User profile not found'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            file_path = reel.video.path
            
            if not os.path.exists(file_path):
                return Response(
                    {'error': 'Video file not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            content_type, encoding = mimetypes.guess_type(file_path)
                
            # Using the ranged_file_response function to handle range requests and serve the video
            response = ranged_file_response(file_path, request, content_type)
            return response
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get', 'post', 'delete'], url_path='comment_likes/(?P<comment_id>[^/.]+)')
    def comment_likes(self, request, pk=None, comment_id=None):
        """Handle likes for a comment"""
        if not comment_id:
            return Response(
                {'detail': 'Comment ID is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        reel = self.get_object()
        
        try:
            comment = ReelComment.objects.get(id=comment_id)
            # Making sure the comment belongs to the reel
            if comment.reel.id != reel.id:
                return Response(
                    {'detail': 'Comment does not belong to this reel.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except ReelComment.DoesNotExist:
            return Response(
                {'detail': 'Comment not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if request.method == 'GET':
            likes = ReelCommentLike.objects.filter(comment=comment)
            serializer = ReelCommentLikeSerializer(
                likes,
                many=True,
                context={'request': request}
            )
            return Response(serializer.data)
        
        elif request.method == 'POST':
            if not request.user.is_authenticated:
                return Response(
                    {'detail': 'Authentication required'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            author = request.user.author_profile
            # Check if already liked
            if ReelCommentLike.objects.filter(comment=comment, author=author).exists():
                return Response(
                    {'detail': 'You have already liked this comment.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            like = ReelCommentLike.objects.create(comment=comment, author=author)
            serializer = ReelCommentLikeSerializer(like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        elif request.method == 'DELETE':
            if not request.user.is_authenticated:
                return Response(
                    {'detail': 'Authentication required'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            author = request.user.author_profile
            try:
                like = ReelCommentLike.objects.get(comment=comment, author=author)
                like.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except ReelCommentLike.DoesNotExist:
                return Response(
                    {'detail': 'You have not liked this comment.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
    
    @action(detail=False, methods=['get'])
    def feed(self, request):
        """Get a feed of reels with visibility filtering"""
        try:
            # You can't open stream feed unless your authenticated
            if not request.user.is_authenticated:
                return Response(
                    {"detail": "Authentication required to view reels feed."},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            try:
                author = request.user.author_profile
            except AttributeError:
                return Response(
                    {"detail": "User profile not found."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            following = Follow.objects.filter(actor=author, isPending=False).values_list('object_id', flat=True)
            queryset = Reel.objects.filter(
                # Show all public reels
                models.Q(visibility='PUBLIC') |
                # Show user's own reels regardless of visibility
                models.Q(author=author) |
                # Show UNLISTED and FRIENDS reels, but only from people the user follows
                (models.Q(visibility__in=['FRIENDS', 'UNLISTED']) & models.Q(author_id__in=following))
            )
            reels = queryset.order_by('-created_at') # Ordering results by creation date
            serializer = self.get_serializer(
                reels, 
                many=True, 
                context={'request': request}
            )
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
