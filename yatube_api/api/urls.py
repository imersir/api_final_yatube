from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

router_v1 = DefaultRouter()
router_v1.register(r'posts', PostViewSet, basename='posts_api')
router_v1.register(r'group', GroupViewSet, basename='group')
router_v1.register(r'follow', FollowViewSet, basename='follow')
router_v1.register(
    r'posts/(?P<id>[0-9]+)/comments', CommentViewSet, basename='comment_api'
)

urlpatterns = [
    path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/', include(router_v1.urls)),
]
