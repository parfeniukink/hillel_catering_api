from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password

from .enums import Role


class UserManager(BaseUserManager):
    def _create_user(self, email: str, password: str, **extra_fields):
        """Create and save a user with passed parameters."""

        email = self.normalize_email(email)
        password = make_password(password)
        user = self.model(email=email, password=password, **extra_fields)
        user.save()

        return user

    def create_user(self, email: str, password: str, **extra_fields):
        extra_fields["is_staff"] = False
        extra_fields["role"] = Role.CLIENT

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields):
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True
        extra_fields["role"] = Role.ADMIN

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=150, unique=True, null=False)
    phone_number = models.CharField(max_length=10, unique=True, null=False)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    date_joined = models.DateTimeField(default=timezone.now)

    role = models.CharField(
        max_length=15,
        default=Role.CLIENT,
        choices=Role.choices(),
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"

    def __str__(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"

        return self.email

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """

        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """Return the short name for the user."""

        return self.first_name
