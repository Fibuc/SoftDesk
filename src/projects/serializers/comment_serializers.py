from rest_framework import serializers

from projects.models import Issue, Comment
from .issue_serializers import IssueCommentSerializer
from authentication.serializers import UserListSerializer


class CommentDetailSerializer(serializers.ModelSerializer):
    """Serializer du détail d'un commentaire."""
    issue = IssueCommentSerializer()
    author = UserListSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'issue', 'author', 'description', 'created_time']


class CommentListSerializer(serializers.ModelSerializer):
    """Serializer de la liste des commentaires."""
    issue = IssueCommentSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'issue', 'description']


class CommentCreateSerializer(serializers.ModelSerializer):
    """Serializer lors de la création d'un commentaire."""
    issue = serializers.PrimaryKeyRelatedField(queryset=Issue.objects.all())
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['author']

    def validate_issue(self, value):
        user = self.context['request'].user
        queryset = Issue.objects.filter(
            id=value.id, project__contributed_by__user=user
            )
        if not queryset.exists():
            raise serializers.ValidationError(
                "L'utilisateur n'est pas contributeur de ce projet."
                )
        return value

    def create(self, validated_data):
        comment = Comment(
            description=validated_data['description'],
            )
        comment.author = self.context['request'].user
        comment.issue = validated_data['issue']
        comment.save()
        return comment


class CommentModifySerializer(serializers.ModelSerializer):
    """Serializer lors de la modification d'un commentaire."""
    class Meta:
        model = Comment
        fields = ['description']
