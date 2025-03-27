import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction

User = get_user_model()


@pytest.mark.django_db
def test_john_is_created(john):
    """
    1. data preparation (payload + expected)
    2. result = action()
    3. optional: update expected
    4. compare result is expected
    """

    assert User.objects.count() == 1


@pytest.mark.parametrize(
    "payload",
    (
        {
            # email is the same
            "email": "john@email.com",
            "password": "@Dm1n#LKJ",
            "phone_number": "...",
        },
        {
            # phone is the same
            "email": "marry@email.com",
            "password": "@Dm1n#LKJ",
            "phone_number": "+380999",
        },
    ),
)
@pytest.mark.django_db
def test_user_duplicate(john, payload):
    with pytest.raises(IntegrityError):

        with transaction.atomic():
            User.objects.create_user(**payload)

    assert User.objects.count() == 1

