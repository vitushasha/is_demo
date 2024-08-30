from django.urls import path

from robot_weather_app.models.robot_model import RobotWeatherModel
from robot_weather_app.views.install import install
from robot_weather_app.views.uninstall import uninstall
from robot_weather_app.views.robot_currency_view import robot_currency

app_name = 'bitrix_robot_weather'

urlpatterns = [
    path('install/', install, name='install'),
    path('uninstall/', uninstall, name='uninstall'),
    path('home/', robot_currency, name='robot_currency'),
    path('handler/', RobotWeatherModel.as_view(), name='handler_robot'),
]