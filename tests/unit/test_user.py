import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction

User = get_user_model()


@pytest.mark.django_db
def test_john_fixture(john):
    assert User.objects.count() == 1


# note: 1 iteration without `parametrized` and `django_db` marker
@pytest.mark.parametrize(
    "payload",
    (
        {
            # same email
            "email": "john@email.com",
            "password": "@Dm1n#LKJ",
            "phone_number": "+3808888",
        },
        {
            # same phone
            "email": "marry@email.com",
            "password": "@Dm1n#LKJ",
            "phone_number": "+3807777",
        },
    ),
)
@pytest.mark.django_db
def test_user_duplicate(john, payload: dict):
    # todo: show without atomic() first
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            instance = User.objects.create_user(**payload)
            print(instance.email)
            print(instance.id)

    assert User.objects.count() == 1
