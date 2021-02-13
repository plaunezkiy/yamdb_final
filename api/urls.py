from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CommentViewSet, ReviewViewSet
from categories.views import CategoryViewSet
from genres.views import GenreViewSet
from users.views import UsersViewSet, email_code, get_token
from titles.views import TitleViewSet

router_v1 = DefaultRouter()
router_v1.register('users', UsersViewSet, basename='users')

router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')

router_v1.register(r'titles/(?P<title_id>[0-9]+)/reviews', ReviewViewSet)
router_v1.register(r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
                   CommentViewSet,
                   basename='comments')

v1_auth = [
    path('token/', get_token, name='token'),
    path('email/', email_code, name='email'),
]

urlpatterns = [
    path('v1/auth/', include(v1_auth)),
    path('v1/', include(router_v1.urls)),
]
