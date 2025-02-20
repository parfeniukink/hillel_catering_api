from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import generics, permissions, serializers, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import routers
from users.enums import Role

from .services import Activator

User = get_user_model()
# == from users.models import User

# def create_user(request: HttpRequest) -> JsonResponse:
#     if request.method != "POST":
#         raise NotImplementedError("Only POST requests")

#     data: dict = json.loads(request.body)
#     user = User.objects.create_user(**data)

#     # convert to dict
#     results = {
#         "id": user.id,
#         "email": user.email,
#         "first_name": user.first_name,
#         "last_name": user.last_name,
#         "role": user.role,
#         "is_active": user.is_active,
#     }

#     return JsonResponse(results)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "phone_number",
            "first_name",
            "last_name",
            "password",
        ]

    def validate(self, attrs: dict) -> dict:
        """Change the password for its hash"""

        attrs["password"] = make_password(attrs["password"])

        return attrs


class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "phone_number", "first_name", "last_name", "role"]


class UserRetrieveCreateAPI(generics.ListCreateAPIView):
    http_method_names = ["get", "post"]
    serializer_class = UserRegistrationSerializer
    # NOTE: what about self.get_permissions_classes ???
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Functional approach
        # import uuid
        # activation_key: uuid.UUID = services.create_activation_key(
        #     email=serializer.data["email"]
        # )
        # services.send_user_activation_email(
        #     email=serializer.data["email"], activation_key=activation_key
        # )

        # OOP approach
        activator_service = Activator(email=serializer.data["email"])
        activation_key = activator_service.create_activation_key()
        activator_service.send_user_activation_email(activation_key=activation_key)
        activator_service.save_activation_information(
            internal_user_id=serializer.instance.id,
            activation_key=activation_key,
        )

        return Response(
            UserPublicSerializer(serializer.validated_data).data,
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(serializer.data),
        )

    def get(self, request):
        user = ...  # NOTE: how to take the user from there? permissions
        serializer = UserSerializer(user)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=self.get_success_headers(serializer.data),
        )


@api_view(http_method_names=["POST"])
def resend_activation_mail(request) -> Response:
    raise NotImplementedError


# ==================================================
# Using Routers and ViewSets
# ==================================================


from rest_framework import viewsets, status

# from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication


class UsersViewSet(viewsets.GenericViewSet):
    authentication_classes = [JWTAuthentication]
    # note: remove and show the `/users` page
    serializer_class = UserRegistrationSerializer

    def get_permissions(self):
        if self.action == "list":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return [permissions.AllowAny()]
        elif self.action == None:
            # for browser page
            return [permissions.AllowAny()]
        else:
            raise NotImplementedError(self.action)

    # @action(methods=["POST"], detail=False)
    def create(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            status=status.HTTP_201_CREATED,
            data=serializer.validated_data,
        )

    # @action(methods=["GET"], detail=False)
    def list(self, request):
        """Return the user itself."""

        serializer = UserPublicSerializer(request.user)
        return Response(serializer.data)


router = routers.DefaultRouter()
router.register(r"users", UsersViewSet, basename="user")
