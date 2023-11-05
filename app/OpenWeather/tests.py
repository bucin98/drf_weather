from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .models import City, CurrentWeather, WeatherForecast
from rest_framework import status
import pytest


@pytest.fixture
def user_with_token():
    user = get_user_model().objects.create(username="testuser")
    token, _ = Token.objects.get_or_create(user=user)
    return user, token


@pytest.mark.django_db
def test_search_current_weather_success(user_with_token):
    user, token = user_with_token
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    url = reverse('search') + '?city=London'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    cities = City.objects.all()
    assert cities.__len__() == 1
    assert cities.first().name == 'London'

    weather = CurrentWeather.objects.all()
    assert weather.__len__() == 1
    assert weather.first().city == cities.first()

    assert response.data['city']['name'] == "London"


@pytest.mark.django_db
def test_search_current_weather_city_not_found(user_with_token):
    user, token = user_with_token
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    url = reverse('search') + '?city=Mwpepw'
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['message'] == 'City not found.'


@pytest.mark.django_db
def test_search_current_weather_no_city_or_zip_code(user_with_token):
    user, token = user_with_token
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    url = reverse('search')
    response = client.get(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['message'] == 'No city or zip_code supplied.'


@pytest.mark.django_db
def test_search_current_weather_zip_code_not_found(user_with_token):
    user, token = user_with_token
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    url = reverse('search') + '?zip=99999999'
    response = client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['message'] == 'City not found.'


@pytest.mark.django_db
def test_current_user_weather_not_set(user_with_token):
    user, token = user_with_token
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    url = reverse('current')
    response = client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['message'] == 'Your location is not set.'


@pytest.mark.django_db
def test_current_user_weather_set_correct(user_with_token):
    user, token = user_with_token
    user.location = 'London'
    user.save()
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    url = reverse('current')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    cities = City.objects.all()
    assert cities.__len__() == 1
    assert cities.first().name == 'London'

    weather = CurrentWeather.objects.all()
    assert weather.__len__() == 1
    assert weather.first().city == cities.first()

    assert response.data['city']['name'] == "London"


@pytest.mark.django_db
def test_current_user_weather_set_non_exist_city(user_with_token):
    user, token = user_with_token
    user.location = 'qewlq'
    user.save()
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    url = reverse('current')
    response = client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['message'] == 'Your location city not found.'


@pytest.mark.django_db
def test_search_forecast_weather_no_city_or_zip_code_no_user_location(user_with_token):
    user, token = user_with_token
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    url = reverse('forecast')
    response = client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['message'] == 'Your location is not set.'


@pytest.mark.django_db
def test_search_forecast_weather_no_city_or_zip_code_user_location(user_with_token):
    user, token = user_with_token
    user.location = 'London'
    user.save()
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    url = reverse('forecast')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    cities = City.objects.all()
    assert cities.__len__() == 1
    assert cities.first().name == 'London'

    weather = WeatherForecast.objects.all()
    assert weather.__len__() == 40
    assert weather.first().city == cities.first()

    assert response.data['city'] == "London"


@pytest.mark.django_db
def test_search_forecast_weather_wrong_city(user_with_token):
    user, token = user_with_token
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    url = reverse('forecast') + '?city=Kqweq'
    response = client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['message'] == 'City not found.'


@pytest.mark.django_db
def test_search_forecast_weather_city(user_with_token):
    user, token = user_with_token
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    url = reverse('forecast') + '?city=London'
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

    cities = City.objects.all()
    assert cities.__len__() == 1
    assert cities.first().name == 'London'

    weather = WeatherForecast.objects.all()
    assert weather.__len__() == 40
    assert weather.first().city == cities.first()

    assert response.data['city'] == "London"
