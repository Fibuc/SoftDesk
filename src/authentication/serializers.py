from rest_framework import serializers
from authentication.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer de la création d'un utilisateur."""
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'birth_date', 'can_be_contacted',
            'can_data_be_shared', 'date_joined'
            ]

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserListSerializer(serializers.ModelSerializer):
    """Serializer de la liste des utilisateurs."""
    class Meta:
        model = User
        fields = ['id', 'username']


class UserModifySerializer(serializers.ModelSerializer):
    """Serializer de modification d'un utilisateur."""
    class Meta:
        model = User
        fields = [
            'id', 'username', 'birth_date', 'can_be_contacted',
            'can_data_be_shared', 'date_joined'
            ]
        read_only_fields = ['birth_date', 'date_joined']


class ChangePasswordSerializer(serializers.ModelSerializer):
    """Serializer du changement de mot de passe."""
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['old_password', 'new_password', 'confirm_password']

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError(
                "Les mots de passe ne correspondent pas."
                )

        if not bool(
            data['old_password']
            and data['new_password']
            and data['confirm_password']
        ):
            raise serializers.ValidationError(
                "Les mots de passe ne correspondent pas."
                )

        return data

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                "Ancien mot de passe incorrect."
                )

        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
