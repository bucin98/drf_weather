import datetime
import pytz
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import City, WeatherForecast
from .api_calls import get_current_weather, get_forecast_weather
from .serializers import CurrentWeatherSerializer, ForecastWeatherSerializer
from django.utils import timezone
from DRF_WEATHER_APP.settings import CURRENT_WEATHER_TIME
from .utils import get_user_location


class ForecastWeather(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        city = request.query_params.get('city')
        if not city:
            city = get_user_location(request)
        if isinstance(city, Response):
            return city

        now = datetime.datetime.now(datetime.timezone.utc)
        city_forecasts = WeatherForecast.objects.filter(city__name=city).order_by('date')
        if city_forecasts and now < city_forecasts.first().date:
            return Response(
                data={'city': city, 'forecast': [ForecastWeatherSerializer(x).data for x in city_forecasts]})

        weather = get_forecast_weather(city)
        if weather:
            return Response(data=weather, status=status.HTTP_200_OK)
        return Response(data={'message': 'City not found.'}, status=status.HTTP_404_NOT_FOUND)


class SearchCurrentWeather(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        city = request.query_params.get('city')
        zip_code = request.query_params.get('zip', None)
        city_zip = city if city else zip_code

        if city:
            city_obj = City.objects.filter(name=city).first()
            zip_code = None  # If city, then no need to associate zip_code=city
        elif zip_code:
            city_obj = City.objects.filter(zipcode__zip_code=zip_code).first()
        else:
            return Response({'message': 'No city or zip_code supplied.'}, status=status.HTTP_400_BAD_REQUEST)

        if not city_obj or not hasattr(city_obj, 'currentweather') or timezone.now() - datetime.timedelta(
                minutes=CURRENT_WEATHER_TIME) > city_obj.currentweather.date:
            weather = get_current_weather(city_zip, zip_code)
            if weather:
                return Response(data=weather, status=status.HTTP_200_OK)
            return Response(data={'message': 'City not found.'}, status=status.HTTP_404_NOT_FOUND)

        return Response(data=CurrentWeatherSerializer(city_obj.currentweather).data, status=status.HTTP_200_OK)


class GetUserLocationWeather(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        User = get_user_model()
        user = User.objects.get(pk=request.user.pk)

        if not user.location:
            return Response({'message': 'Your location is not set.'}, status=status.HTTP_404_NOT_FOUND)

        city = City.objects.filter(name=user.location).first()
        if not city or not hasattr(city, 'currentweather') or timezone.now() - datetime.timedelta(
                minutes=CURRENT_WEATHER_TIME) > city.currentweather.date:
            weather = get_current_weather(user.location)
            if weather:
                return Response(data=weather, status=status.HTTP_200_OK)
            return Response(data={'message': 'Your location city not found.'}, status=status.HTTP_404_NOT_FOUND)

        return Response(data=CurrentWeatherSerializer(city.currentweather).data, status=status.HTTP_200_OK)
