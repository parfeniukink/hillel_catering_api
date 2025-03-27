import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def john():
    return User.objects.create_user(
        **dict(
            email="john@email.com",
            password="john",
            phone_number="+380999",
            first_name="John",
            last_name="Doe",
        )
    )
