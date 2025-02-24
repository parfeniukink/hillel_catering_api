from rest_framework import status, permissions, viewsets, routers
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.services import Activator

from .serializers import UserRegistratrionSerializer, UserPublicSerializer


class UserAPIViewSet(viewsets.GenericViewSet):
    authentication_classes = [JWTAuthentication]
    serializer_class = UserRegistratrionSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action == "list":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return [permissions.AllowAny()]
        elif self.action == None:
            return [permissions.AllowAny()]
        else:
            raise NotImplementedError(f"Action {self.action} is not ready yet")

    def create(self, request):
        serializer = UserRegistratrionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # SEND THE ACTIVATION LINK TO THE EMAIL
        # Functional approach
        # activation_key: uuid.UUID = services.create_activation_key(
        #     email=serializer.data["email"]
        # )
        # services.send_user_activation_email(
        #     email=serializer.data["email"], activation_key=activation_key
        # )

        # OOP approach
        activator_service = Activator(email=getattr(serializer.instance, "email"))
        activation_key = activator_service.create_activation_key()
        activator_service.send_user_activation_email(activation_key=activation_key)
        activator_service.save_activation_information(
            internal_user_id=getattr(serializer.instance, "id"),
            activation_key=activation_key,
        )

        return Response(
            UserPublicSerializer(serializer.validated_data).data,
            status=status.HTTP_201_CREATED,
        )

    def list(self, request):
        return Response(
            UserPublicSerializer(request.user).data,
            status=status.HTTP_200_OK,
        )


router = routers.DefaultRouter()
router.register(r"users", UserAPIViewSet, basename="user")
