from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status

from authentication.models import User
from authentication.permissions import IsAnonymous, IsUser
from authentication.serializers import (
    UserCreateSerializer,
    UserListSerializer,
    UserModifySerializer,
    ChangePasswordSerializer
    )


class UserViewSet(ModelViewSet):
    """Classe du ViewSet des utilisateurs."""
    serializer_class = UserListSerializer
    create_serializer_class = UserCreateSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return self.create_serializer_class

        return super().get_serializer_class()

    def get_permissions(self):
        match self.action:
            case 'list':
                return [IsAuthenticated()]
            case 'create':
                return [IsAnonymous()]
            case _:
                return [IsAdminUser()]

    def get_queryset(self):
        return User.objects.all().exclude(is_superuser=True)


class AccountView(RetrieveAPIView):
    """Classe de la vue en modalité 'détails' du compte utilisateur."""
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
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
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response()


class NewPasswordView(UpdateAPIView):
    """
    Classe de la vue en modalité 'mise à jour' du nouveau mot de passe
    utilisateur.
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsUser]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user
