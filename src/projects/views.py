from pprint import pprint
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from projects.models import Project, Issue, Comment, Contributor
from projects.serializers import ProjectDetailSerializer, IssueDetailSerializer, CommentDetailSerializer, ContributorSerializer, IssueCreateSerializer
from projects.serializers import ProjectListSerializer, IssueListSerializer, CommentListSerializer

from projects.permissions import IsAuthorOrReadOnly, IsContributor


class MultipleSerializerMixin:
    
    detail_serializer_class = None
    create_serializer_class = None
    modify_serializer_class = None

    def get_serializer_class(self):
        """Selectionne le serializer automatiquement selon le type d'action effectué.

        Returns:
            Serializer: Serializer correspondant à l'action.
        """
        if self.action == 'retrieve' and self.create_serializer_class is not None:
            print('detail_serializer_class')
            return self.detail_serializer_class
        elif self.action == 'create' and self.create_serializer_class is not None:
            print('create_serializer_class')
            return self.create_serializer_class
        elif self.action in ['update', 'partial_update'] and self.detail_serializer_class is not None:
            print('modify_serializer_class')
            return self.modify_serializer_class
        else:
            print('super().get_serializer_class()')
            return super().get_serializer_class()


class ContributorViewSet(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = ContributorSerializer

    def get_queryset(self):
        return Contributor.objects.all()


class ProjectViewSet(MultipleSerializerMixin, ModelViewSet):

    detail_serializer_class = ProjectDetailSerializer
    serializer_class = ProjectListSerializer
    permission_classes = [IsAuthenticated, IsContributor, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Project.objects.filter(contributed_by__user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IssueViewSet(MultipleSerializerMixin, ModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    create_serializer_class = IssueCreateSerializer
    permission_classes = [IsAuthenticated, IsContributor, IsAuthorOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Issue.objects.filter(project__contributed_by__user=user)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    

class CommentViewSet(MultipleSerializerMixin, ModelViewSet):

    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer
    permission_classes = [IsAuthenticated, IsContributor, IsAuthorOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Comment.objects.filter(issue__project__contributed_by__user=user)