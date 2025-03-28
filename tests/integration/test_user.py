import pytest
from django.contrib.auth import get_user_model
from django.test.client import Client
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
def test_john_creation(client: Client):
    payload = {
        "email": "john@email.com",
        "password": "@Dm1n#LKJ",
        "phone_number": "...",
        "first_name": "John",
        "last_name": "Doe",
    }

    response = client.post(path="/users/", data=payload)

    john = User.objects.get(id=response.json()["id"])

    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert User.objects.count() == 1
    assert john.id == john.pk == response.json()["id"]
    assert john.first_name == response.json()["first_name"]
    assert john.last_name == response.json()["last_name"]
