import django_filters.rest_framework
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination

from .filters import TitleFilter
from .models import Category, Genre, Review, Title
from .permissions import IsAdminOrReadOnly, IsAuthorAdminModeratorOrReadOnly
from .serializers import (CategorySerializer, CommentsSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer)

PERMISSION_CLASSES = [
    permissions.IsAuthenticatedOrReadOnly,
    IsAdminOrReadOnly
]


class BaseModelClasses(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Limits API methods to GET, POST, DELETE
    """
    pass


class TitleViewSet(viewsets.ModelViewSet):
    """
    A class that allows all users to get data about titles,
    and for admins to create and delete titles using the API
    """
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = PERMISSION_CLASSES
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    pagination_class = PageNumberPagination
    filterset_class = TitleFilter


class CategoryViewSet(BaseModelClasses):
    """
    A class that allows all users to get data about categories of titles,
    and for admins to create and delete categories using the API
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = PERMISSION_CLASSES
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,
                       filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class GenreViewSet(BaseModelClasses):
    """
    A class that allows all users to get data about genres of titles,
    and for admins to create and delete genres using the API
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = PERMISSION_CLASSES
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend,
                       filters.SearchFilter]
    filterset_fields = ['name', ]
    search_fields = ['name', ]
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthorAdminModeratorOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly
    )

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(
            author=self.request.user,
            title=title
        )

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.review.all()


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = (
        IsAuthorAdminModeratorOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly
    )

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comment.all()
