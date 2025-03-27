import random

from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, routers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.service import Activator

from .serializers import (
    UserActivationSerializer,
    UserPublicSerializer,
    UserRegistratrionSerializer,
)

# PoC
# @celery_app.task
# def background_task(n: int):
#     print(f"Running in the background, {n=}")
#     return n


class UserAPIViewSet(viewsets.GenericViewSet):
    authentication_classes = [JWTAuthentication]
    serializer_class = UserRegistratrionSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == "list":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return [permissions.AllowAny()]
        elif self.action == None:
            return [permissions.AllowAny()]
        elif self.action == "activate":
            return [permissions.AllowAny()]
        else:
            raise NotImplementedError(f"Action {self.action} is not ready yet")

    def create(self, request):
        """Create a new User."""
        serializer = UserRegistratrionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        service = Activator(email=getattr(serializer.instance, "email"))
        activation_key = service.create_activation_key()
        service.save_activation_information(
            user_id=getattr(serializer.instance, "id"),
            activation_key=activation_key,
        )
        service.send_user_activation_email(activation_key=activation_key)

        return Response(
            UserPublicSerializer(serializer.instance).data,
            status=status.HTTP_201_CREATED,
        )

    @swagger_auto_schema(
        responses={
            200: UserPublicSerializer,
        },
    )
    def list(self, request):
        """Retrieve User information."""

        return Response(
            UserPublicSerializer(request.user).data,
            status=status.HTTP_200_OK,
        )

    # note: fixing default swagger schema
    @swagger_auto_schema(
        method="post",
        request_body=UserActivationSerializer,
        responses={
            204: {},
        },
    )
    @action(methods=["POST"], detail=False)
    def activate(self, request):
        serializer = UserActivationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = Activator()
        service.activate_user(
            activation_key=serializer.validated_data.get("key")
        )

        # serializer.validated_data
        return Response(data=None, status=status.HTTP_204_NO_CONTENT)


router = routers.DefaultRouter()
router.register(r"users", UserAPIViewSet, basename="user")
