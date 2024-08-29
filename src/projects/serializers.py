from rest_framework import serializers

from projects.models import Project, Issue, Comment, Contributor
from authentication.models import User
from authentication.serializers import UserListSerializer


class ContributorProjectSerializer(serializers.ModelSerializer):
    """Serializer des contributeurs d'un projet."""
    user = UserListSerializer()

    class Meta:
        model = Contributor
        fields = ['user']


class ProjectListSerializer(serializers.ModelSerializer):
    """Serializer de la liste des projets."""
    author = UserListSerializer()

    class Meta:
        model = Project
        fields = '__all__'


class ProjectDetailSerializer(serializers.ModelSerializer):
    """Serializer du détail d'un projet."""
    author = UserListSerializer()
    contributors = ContributorProjectSerializer(
        source='contributed_by', many=True
        )
    nb_of_issues = serializers.IntegerField(source='issues.count')

    class Meta:
        model = Project
        fields = '__all__'


class ProjectModifyCreateSerializer(serializers.ModelSerializer):
    """Serializer lors de la modification ou création d'un projet."""
    author = UserListSerializer(read_only=True)
    contributors = ContributorProjectSerializer(
        source='contributed_by', many=True, read_only=True
        )
    nb_of_issues = serializers.IntegerField(
        source='issues.count', read_only=True
        )

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['author', 'contributors', 'created_time']


class ProjectIssueSerializer(serializers.ModelSerializer):
    """Serializer du projet lors de son affichage dans les demandes."""

    class Meta:
        model = Project
        fields = ['id', 'name']


class ContributorSerializer(serializers.ModelSerializer):
    """Serializer des contributeurs."""
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all().exclude(is_superuser=True)
        )

    class Meta:
        model = Contributor
        fields = '__all__'
        read_only_fields = ['project']

    def validate(self, data):
        user = data['user']
        project = self.context['project']
        if project.is_contributor(user=user):
            raise serializers.ValidationError(
                "L'utilisateur est déjà contributeur du projet."
                )

        return data

    def create(self, project):
        self.validated_data['project'] = project
        return Contributor.objects.create(**self.validated_data)


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
