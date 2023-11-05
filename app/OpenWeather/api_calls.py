import datetime
import pytz
import requests
from DRF_WEATHER_APP.settings import OP_WEATHER_API_KEY
from .models import CurrentWeather, City, ZipCode, WeatherForecast
from .serializers import CurrentWeatherSerializer, ForecastWeatherSerializer
from django.utils import timezone


def save_forecast_weather(response):
    city_name = response['city']['name']
    forecasts = [(x['dt'], x['main']['temp'], x['weather'][0]['main']) for x in
                 response['list']]  # (datetime, temp, weather)
    city, _ = City.objects.get_or_create(name=city_name)
    all_obj = []
    for forecast_data in forecasts:
        date, temperature, weather_condition = forecast_data
        date = datetime.datetime.fromtimestamp(date, tz=datetime.timezone.utc)
        weather_obj, _ = WeatherForecast.objects.get_or_create(
            city=city,
            date=date,
            temperature=temperature,
            weather_condition=weather_condition
        )
        all_obj.append(weather_obj)
    old_forecasts = WeatherForecast.objects.filter(city=city).exclude(
        pk__in=[item.pk for item in all_obj])
    old_forecasts.delete()
    return {'city': city_name, 'forecast': [ForecastWeatherSerializer(x).data for x in all_obj]}


def save_current_weather(response, zip_code):
    city_name = response['name']
    temperature = response['main']['temp']
    weather_condition = response['weather'][0]['main']
    city, created = City.objects.get_or_create(name=city_name)
    if zip_code:
        ZipCode.objects.get_or_create(zip_code=zip_code, city=city)
    current_weather, _ = CurrentWeather.objects.update_or_create(city=city,
                                                                 defaults={
                                                                     'date': timezone.now(),
                                                                     'temperature': temperature,
                                                                     'weather_condition': weather_condition})
    current_weather.save()
    return current_weather


def get_current_weather(city_zip, zip_code=None):  # City name/ Zip code
    api_url = f'https://api.openweathermap.org/data/2.5/weather?q={city_zip}&APPID={OP_WEATHER_API_KEY}&units=metric'
    result = make_request(api_url)
    if result:
        weather = save_current_weather(result, zip_code)
        return CurrentWeatherSerializer(weather).data
    return None


def get_forecast_weather(city_zip):
    api_url = f'https://api.openweathermap.org/data/2.5/forecast?q={city_zip}&APPID={OP_WEATHER_API_KEY}&units=metric'
    result = make_request(api_url)
    if result:
        weather = save_forecast_weather(result)
        return weather
    return None


def make_request(api_url):
    response = requests.get(api_url)

    if response.status_code == 200:
        weather_data = response.json()
        return weather_data
    else:
        return None
