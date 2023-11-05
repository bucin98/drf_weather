from rest_framework import serializers
from .models import CurrentWeather, City, WeatherForecast


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['name']


class CurrentWeatherSerializer(serializers.ModelSerializer):
    city = CitySerializer()

    class Meta:
        model = CurrentWeather
        fields = ['city', 'date', 'temperature', 'weather_condition']


class ForecastWeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherForecast
        fields = ['date', 'temperature', 'weather_condition']
