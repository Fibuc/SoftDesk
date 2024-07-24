from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from projects.views import ProjectViewSet, IssueViewSet, CommentViewSet, ContributorViewSet
from authentication.views import UserViewSet

router = routers.SimpleRouter()

router.register('project', ProjectViewSet, basename='project')
router.register('issue', IssueViewSet, basename='issue')
router.register('comment', CommentViewSet, basename='comment')
router.register('user', UserViewSet, basename='user')
router.register('contributor', ContributorViewSet, basename='contributor')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
]
