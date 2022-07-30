from product.models import Comment
from product.serializer import CommentSerializer
from rest_framework import generics
from helpers.pagination import CustomPagination
from rest_framework.permissions import IsAuthenticated

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers


# Create your views here.
class UserCommentsView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CustomPagination

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)

        return queryset

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_headers("Authorization", ))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)
