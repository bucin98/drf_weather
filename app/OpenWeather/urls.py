from django.urls import path
from .views import GetUserLocationWeather, SearchCurrentWeather, ForecastWeather

urlpatterns = [
    path('current', GetUserLocationWeather.as_view(), name='current'),
    path('search', SearchCurrentWeather.as_view(), name='search'),
    path('forecast', ForecastWeather.as_view(), name='forecast')
]
