from django.urls import include, path

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import CustomTokenObtainPair
from users.views import RegistrationViewSet, UsersViewSet

from .views import (CategoryViewSet, CommentsViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet)


router_v1 = DefaultRouter()
router_v1.register('auth/email', RegistrationViewSet)
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments',
)
router_v1.register('titles', TitleViewSet)
router_v1.register('users', UsersViewSet, basename='users')


urlpatterns = [
    path(
        'v1/auth/token/',
        TokenObtainPairView.as_view(serializer_class=CustomTokenObtainPair),
    ),
    path('v1/', include(router_v1.urls)),
]
