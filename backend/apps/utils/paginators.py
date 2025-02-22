from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class AuthorsPaginator(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'
    object_type = 'authors'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'type': self.object_type,
            self.object_type: data
        })

class PostsPaginator(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'
    object_type = 'posts'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'type': self.object_type,
            'src': data
        })

class LikesPaginator(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'size'
    object_type = 'likes'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'type': self.object_type,
            'src': data
        })