from rest_framework.serializers import ModelSerializer, IntegerField

from projects.models import Project, Issue, Comment, Contributor
from authentication.serializers import UserListSerializer


class ContributorProjectSerializer(ModelSerializer):

    user = UserListSerializer()
    
    class Meta:
        model = Contributor
        fields = ['id', 'user']


class ProjectListSerializer(ModelSerializer):

    author = UserListSerializer()

    class Meta:
        model = Project
        fields = ['id', 'name', 'author', 'created_time']


class ProjectDetailSerializer(ModelSerializer):

    author = UserListSerializer()
    contributors = ContributorProjectSerializer(source='contributed_by', many=True)
    nb_of_issues = IntegerField(source='issues.count', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'author', 'description', 'type', 'contributors', 'nb_of_issues', 'created_time']


class ContributorSerializer(ModelSerializer):
    
    user = UserListSerializer()
    project = ProjectListSerializer()

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'created_time']


class IssueListSerializer(ModelSerializer):

    project = ProjectListSerializer()
    author = UserListSerializer()

    class Meta:
        model = Issue
        fields = ['id', 'name', 'project', 'author']


class IssueDetailSerializer(ModelSerializer):

    project = ProjectListSerializer()
    author = UserListSerializer()
    nb_of_comments = IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Issue
        fields = ['id', 'name', 'project', 'author', 'description', 'priority', 'type', 'progress', 'nb_of_comments','created_time']


class CommentDetailSerializer(ModelSerializer):

    issue = IssueListSerializer()
    author = UserListSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'issue', 'author', 'description', 'created_time']


class CommentListSerializer(ModelSerializer):

    issue = IssueListSerializer()
    author = UserListSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'issue', 'author']
