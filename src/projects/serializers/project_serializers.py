from rest_framework import serializers

from projects.models import Project
from .contributor_serializers import ContributorProjectSerializer
from authentication.serializers import UserListSerializer


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
