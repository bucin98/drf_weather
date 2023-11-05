import pytest
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from .models import CustomUser
from .serializers import UserSerializer, UserLocationSerializer


@pytest.fixture
def user_data():
    return {
        'username': 'testuser',
        'password': 'testpassword',
    }


@pytest.fixture
def authenticated_user(user_data):
    user = get_user_model().objects.create_user(**user_data)
    token, _ = Token.objects.get_or_create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    return {"user": user, "client": client}


@pytest.fixture
def create_user(user_data):
    return CustomUser.objects.create_user(**user_data)


@pytest.mark.django_db
def test_user_register(client, user_data):
    url = reverse('register')
    response = client.post(url, user_data, format='json')
    assert response.status_code == 201
    assert CustomUser.objects.count() == 1


@pytest.mark.django_db
def test_login(client, user_data, create_user):
    url = reverse('login')
    response = client.post(url, user_data, format='json')
    assert response.status_code == 200
    assert response.data['token']


@pytest.mark.django_db
def test_user_profile_update(authenticated_user):
    user = authenticated_user["user"]
    client = authenticated_user["client"]
    url = reverse('profile')
    new_location = "New Location"
    data = {'location': new_location}
    response = client.put(url, data, format='json')
    assert response.status_code == 200
    user.refresh_from_db()
    assert user.location == new_location


@pytest.mark.django_db
def test_user_location_serializer():
    location_data = {'location': 'Test Location'}
    serializer = UserLocationSerializer(data=location_data)
    assert serializer.is_valid()
    assert serializer.save()


@pytest.mark.django_db
def test_user_serializer():
    user_data = {'username': 'testuser', 'password': 'testpassword'}
    serializer = UserSerializer(data=user_data)
    assert serializer.is_valid()
    user = serializer.save()
    assert isinstance(user, CustomUser)
