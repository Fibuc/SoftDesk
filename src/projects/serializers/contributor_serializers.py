from rest_framework import serializers

from authentication.models import User
from projects.models import Contributor
from authentication.serializers import UserListSerializer


class ContributorProjectSerializer(serializers.ModelSerializer):
    """Serializer des contributeurs d'un projet."""
    user = UserListSerializer()

    class Meta:
        model = Contributor
        fields = ['user']


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
