from rest_framework.serializers import ModelSerializer
from authentication.models import User


class UserDetailSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'birth_date', 'can_be_contacted', 'can_data_be_shared', 'date_joined']


class UserListSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'username']