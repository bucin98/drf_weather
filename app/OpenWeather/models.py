from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ZipCode(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    zip_code = models.IntegerField()


class CurrentWeather(models.Model):
    city = models.OneToOneField(City, on_delete=models.CASCADE)
    date = models.DateTimeField()
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    weather_condition = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.city} - {self.date} Current"


class WeatherForecast(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    date = models.DateTimeField()
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    weather_condition = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.city} - {self.date} Forecast"
