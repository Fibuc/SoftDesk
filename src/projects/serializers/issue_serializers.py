from rest_framework import serializers

from projects.models import Project, Issue
from .project_serializers import ProjectIssueSerializer
from authentication.serializers import UserListSerializer


class IssueListSerializer(serializers.ModelSerializer):
    """Serializer de la liste des demandes."""
    project = ProjectIssueSerializer()
    author = UserListSerializer()

    class Meta:
        model = Issue
        fields = ['id', 'name', 'project', 'author', 'progress']


class IssueDetailSerializer(serializers.ModelSerializer):
    """Serializer du détail des demandes."""
    project = ProjectIssueSerializer()
    author = UserListSerializer()
    nb_of_comments = serializers.IntegerField(source='comments.count')

    class Meta:
        model = Issue
        fields = [
            'id', 'name', 'project', 'author', 'description', 'priority',
            'type', 'progress', 'nb_of_comments', 'created_time'
            ]


class IssueCreateSerializer(serializers.ModelSerializer):
    """Serializer lors de la création d'une demande."""
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all()
        )
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    nb_of_comments = serializers.IntegerField(
        source='comments.count', read_only=True
        )

    class Meta:
        model = Issue
        fields = '__all__'
        read_only_fields = ['author', 'nb_of_comments']

    def validate_project(self, value):
        user = self.context['request'].user
        queryset = Project.objects.filter(
            id=value.id, contributed_by__user=user
            )
        if not queryset.exists():
            raise serializers.ValidationError(
                "L'utilisateur n'est pas contributeur de ce projet."
                )
        return value

    def create(self, validated_data):
        issue = Issue(
            name=validated_data['name'],
            description=validated_data['description'],
            priority=validated_data['priority'],
            type=validated_data['type'],
            progress=validated_data['progress'],
            )
        issue.author = self.context['request'].user
        issue.project = validated_data['project']
        issue.save()
        return issue


class IssueModifySerializer(serializers.ModelSerializer):
    """Serializer lors de la modification d'une demande."""
    class Meta:
        model = Issue
        fields = ['name', 'description', 'priority', 'type', 'progress']


class IssueCommentSerializer(serializers.ModelSerializer):
    """Serializer de la demande lors de son affichage dans les commentaires."""
    project = ProjectIssueSerializer()

    class Meta:
        model = Issue
        fields = ['id', 'name', 'project']
