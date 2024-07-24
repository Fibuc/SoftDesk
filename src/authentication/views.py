from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from authentication.models import  User
from authentication.serializers import UserDetailSerializer, UserListSerializer
from projects.views import MultipleSerializerMixin


class UserViewSet(MultipleSerializerMixin, ReadOnlyModelViewSet):

    serializer_class = UserListSerializer
    detail_serializer_class = UserDetailSerializer

    def get_queryset(self):
        return User.objects.all()

    @action(detail=True, methods=['patch'])
    def update_contact_status(self, request, pk):
        self.get_object().update_contact_status()
        return Response()