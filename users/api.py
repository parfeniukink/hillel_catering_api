from django.contrib.auth.hashers import make_password
from rest_framework import generics, serializers, status, permissions
from rest_framework.response import Response

from .models import User


# import json
# def create_user(request):
#     if request.method != "POST":
#         raise NotImplementedError
#     data = json.loads(request.body)
#     uesr = User.objects.create_user(**data)
#     results = {
#         "id": user.id,
#         "email": user.email,
#     }
#     return JsonResponse(results)


# 1 - bad idea
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = "__all__"


# class UserRegistratrionSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     phone_number = serializers.CharField()
#     first_name = serializers.CharField()
#     last_name = serializers.CharField()
#     password = serializers.CharField()
#
#     def save(self):
#         self.model.save()


class UserRegistratrionSerializer(serializers.ModelSerializer):
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
        """Change the password for its hash to make token validation available"""

        attrs["password"] = make_password(attrs["password"])

        return attrs


class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "phone_number", "first_name", "last_name", "role"]


# /users: GET POST
class UserCreateRetrieveAPI(generics.ListCreateAPIView):
    http_method_names = ["get", "post"]
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistratrionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(
            UserPublicSerializer(serializer.validated_data).data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def get(self, request):
        user = request.user
        serializer = UserPublicSerializer(user)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=self.get_success_headers(serializer.data),
        )
