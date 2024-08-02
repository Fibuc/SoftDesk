from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status

from authentication.models import  User
from authentication.serializers import (
    UserDetailSerializer,
    UserListSerializer,
    UserModifySerializer,
    ChangePasswordSerializer
    )
from authentication.permissions import IsAnonymous, IsUser


class UserViewSet(ModelViewSet):

    serializer_class = UserListSerializer
    detail_serializer_class = UserDetailSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return self.detail_serializer_class
        
        return super().get_serializer_class()

    def get_permissions(self):
        match self.action:
            case 'list':
                return [IsAuthenticated()]
            case 'create':
                return [IsAnonymous()]
            case _ :
                return [IsAdminUser()]
            

    def get_queryset(self):
        return User.objects.all().exclude(is_superuser=True)
    
    def perform_create(self, serializer):
        """Ajoute le hashage du mot de passe lors de la création d'un nouvel utilisateur.

        Args:
            serializer (UserCreateSerializer): Serializer de la création d'utilisateur.
        """
        user = serializer.save()
        user.set_password(serializer.validated_data.get('password'))
        user.save()


class AccountView(RetrieveAPIView):

    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    modify_serializer_class = UserModifySerializer
    permission_classes = [IsAuthenticated, IsUser]

    def get_object(self):
        return self.request.user
    
    def get_serializer_class(self):
        match self.request.method:
            case 'GET':
                return self.serializer_class
            case 'PATCH':
                return self.modify_serializer_class
    
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ChangePasswordView(UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsUser]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user
