from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework.viewsets import GenericViewSet, ViewSet

from api.v1.filters.user import UserFilter
from api.v1.serializers.user import UserListSerializer, UserCreateSerializer, UserUpdateSerializer
from apps.common.helpers.pagination import CustomPagination
from apps.user.models import User
from apps.user.permission import CustomPermission


class UserMeView(RetrieveAPIView):
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=HTTP_200_OK)


class UserViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = (CustomPermission,)
    pagination_class = CustomPagination
    filterset_class = UserFilter

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        if self.action == "update":
            return UserUpdateSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserListSerializer(user).data, status=HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserListSerializer(instance).data, status=HTTP_200_OK)


class UserActionViewSet(ViewSet):
    permission_classes = (CustomPermission,)
    serializer_class = None
    queryset = User.objects.all()

    perms_map = {
        'POST': ['account_management_create'],
    }

    def block(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        user.is_active = False
        user.blocked_at = datetime.datetime.now()
        user.save()
        return Response(status=HTTP_200_OK)

    def unblock(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        user.is_active = True
        user.blocked_at = None
        user.save()
        return Response(status=HTTP_200_OK)