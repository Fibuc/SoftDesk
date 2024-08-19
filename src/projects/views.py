from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from projects.models import Project, Issue, Comment, Contributor
from projects.serializers import (
    ProjectDetailSerializer, IssueDetailSerializer, CommentDetailSerializer,
    ContributorSerializer, IssueCreateSerializer,
    ProjectModifyCreateSerializer, ProjectListSerializer, IssueListSerializer,
    CommentListSerializer, CommentCreateSerializer, IssueModifySerializer,
    CommentModifySerializer
    )
from projects.permissions import IsAuthorOrReadOnly, IsContributor
from authentication.models import User


class MultipleSerializerMixin:
    """Classe permettant la sélection du serializer."""
    detail_serializer_class = None
    create_serializer_class = None
    modify_serializer_class = None

    def get_serializer_class(self):
        """Selectionne le serializer automatiquement selon le type d'action
        effectué.

        Returns:
            Serializer: Serializer correspondant à l'action.
        """
        if (
            self.action == 'retrieve'
            and self.create_serializer_class is not None
        ):
            return self.detail_serializer_class
        elif (
            self.action == 'create'
            and self.create_serializer_class is not None
        ):
            return self.create_serializer_class
        elif (
            self.action in ['update', 'partial_update']
            and self.detail_serializer_class is not None
        ):
            return self.modify_serializer_class
        else:
            return super().get_serializer_class()


class ProjectContributorsView(APIView):
    """APIView pour créer et supprimer des contributeurs d'un projet."""
    permission_classes = [IsAuthenticated, IsContributor, IsAuthorOrReadOnly]

    def post(self, request, *args, **kwargs):
        project = Project.objects.get(id=kwargs['project_id'])
        serializer = ContributorSerializer(
            data=request.data, context={'project': project}
            )
        if serializer.is_valid():
            serializer.create(project)
            return Response(
                {'valid': 'Le contributeur à été créé avec succès.'},
                status=status.HTTP_201_CREATED
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        project = Project.objects.get(id=kwargs['project_id'])
        user = User.objects.get(id=request.data['user'])
        contributor = Contributor.objects.filter(user=user, project=project)
        if contributor.exists():
            contributor.delete()
            return Response(
                {'valid': 'Le contributeur à été supprimé avec succès.'},
                status=status.HTTP_204_NO_CONTENT
                )

        return Response(
            {'error': "Aucun contributeur n'a été trouvé avec cet ID."},
            status=status.HTTP_400_BAD_REQUEST
            )


class ProjectViewSet(MultipleSerializerMixin, ModelViewSet):
    """ViewSet d'un projet."""
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    create_serializer_class = ProjectModifyCreateSerializer
    modify_serializer_class = ProjectModifyCreateSerializer
    permission_classes = [IsAuthenticated, IsContributor, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Project.objects.filter(contributed_by__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IssueViewSet(MultipleSerializerMixin, ModelViewSet):
    """ViewSet d'une demande."""
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    create_serializer_class = IssueCreateSerializer
    modify_serializer_class = IssueModifySerializer
    permission_classes = [IsAuthenticated, IsContributor, IsAuthorOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Issue.objects.filter(project__contributed_by__user=user)


class CommentViewSet(MultipleSerializerMixin, ModelViewSet):
    """ViewSet d'un commentaire."""
    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer
    create_serializer_class = CommentCreateSerializer
    modify_serializer_class = CommentModifySerializer
    permission_classes = [IsAuthenticated, IsContributor, IsAuthorOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Comment.objects.filter(
            issue__project__contributed_by__user=user
            )
