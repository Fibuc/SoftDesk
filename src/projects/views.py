from rest_framework.viewsets import ReadOnlyModelViewSet

from projects.models import Project, Issue, Comment, Contributor
from projects.serializers import ProjectDetailSerializer, IssueDetailSerializer, CommentDetailSerializer, ContributorSerializer
from projects.serializers import ProjectListSerializer, IssueListSerializer, CommentListSerializer


class MultipleSerializerMixin:
    
    detail_serializer_class = None

    def get_serializer_class(self):
        """Selectionne le serializer automatiquement selon s'il s'agit de la liste ou du détail.

        Returns:
            ProjectListSerializer | ProjectDetailSerializer: Serializer correspondant.
        """
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ContributorViewSet(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = ContributorSerializer

    def get_queryset(self):
        return Contributor.objects.all()


class ProjectViewSet(MultipleSerializerMixin, ReadOnlyModelViewSet):

    detail_serializer_class = ProjectDetailSerializer
    serializer_class = ProjectListSerializer

    def get_queryset(self):
        return Project.objects.all()


class IssueViewSet(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):
        return Issue.objects.all()
    

class CommentViewSet(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer

    def get_queryset(self):
        return Comment.objects.all()
