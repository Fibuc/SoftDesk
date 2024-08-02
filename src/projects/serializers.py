from rest_framework import serializers

from projects.models import Project, Issue, Comment, Contributor
from authentication.serializers import UserListSerializer


class ContributorProjectSerializer(serializers.ModelSerializer):

    user = UserListSerializer()
    
    class Meta:
        model = Contributor
        fields = ['id', 'user']


class ProjectListSerializer(serializers.ModelSerializer):

    author = UserListSerializer()

    class Meta:
        model = Project
        fields = '__all__'


class ProjectDetailSerializer(serializers.ModelSerializer):

    author = UserListSerializer(read_only=True)
    contributors = ContributorProjectSerializer(source='contributed_by', many=True, read_only=True)
    nb_of_issues = serializers.IntegerField(source='issues.count', read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['author', 'contributors', 'created_time']


class ContributorSerializer(serializers.ModelSerializer):
    
    user = UserListSerializer()
    project = ProjectListSerializer()

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'created_time']


class IssueListSerializer(serializers.ModelSerializer):

    project = ProjectListSerializer()
    author = UserListSerializer()

    class Meta:
        model = Issue
        fields = ['id', 'name', 'project', 'author']


class IssueDetailSerializer(serializers.ModelSerializer):

    project = ProjectListSerializer()
    author = UserListSerializer()
    nb_of_comments = serializers.IntegerField(source='comments.count')

    class Meta:
        model = Issue
        fields = ['id', 'name', 'project', 'author', 'description', 'priority', 'type', 'progress', 'nb_of_comments', 'created_time']


class IssueCreateSerializer(serializers.ModelSerializer):

    project = ProjectListSerializer(read_only=True)
    author = UserListSerializer(read_only=True)
    nb_of_comments = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Issue
        fields = ['id', 'name', 'project', 'author', 'description', 'priority', 'type', 'progress', 'nb_of_comments', 'created_time']

    def validate_project(self, value):
        user = self.context['request'].user
        projects = Project.objects.filter(id=value.id, contributed_by__user=user)
        print(projects)
        if not Project.objects.filter(id=value.id, contributed_by__user=user).exists():
            raise serializers.ValidationError("L'utilisateur n'est pas contributeur de ce projet.")
        return value


class CommentDetailSerializer(serializers.ModelSerializer):

    issue = IssueListSerializer()
    author = UserListSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'issue', 'author', 'description', 'created_time']


class CommentListSerializer(serializers.ModelSerializer):

    issue = IssueListSerializer()
    author = UserListSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'issue', 'author']
