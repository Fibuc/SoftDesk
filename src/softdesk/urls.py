from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from projects.views import (
    ProjectViewSet, IssueViewSet, CommentViewSet, ProjectContributorsView
    )
from authentication.views import UserViewSet, AccountView, NewPasswordView
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
    )

router = routers.SimpleRouter()
# Endpoints créés par le router.
router.register('project', ProjectViewSet, basename='project')
router.register('issue', IssueViewSet, basename='issue')
router.register('comment', CommentViewSet, basename='comment')
router.register('user', UserViewSet, basename='user')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path(
        'api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'
        ),
    path(
        'api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'
        ),
    path('api/account/', AccountView.as_view(), name='account'),
    path(
        'api/account/change_password/', NewPasswordView.as_view(),
        name='change_password'
        ),
    path(
        'api/project/<int:project_id>/contributors/',
        ProjectContributorsView.as_view(), name='contributors'
        ),
    path('api/', include(router.urls)),
]
