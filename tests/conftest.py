import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def john():
    return User.objects.create_user(
        email="john@email.com",
        password="john",
        phone_number="+3807777",
    )
