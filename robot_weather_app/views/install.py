from django.http import HttpResponse

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from robot_weather_app.models.robot_model import RobotWeatherModel

@main_auth(on_cookies=True)
def install(request):
    try:
        but = request.bitrix_user_token
        RobotWeatherModel.install_or_update('bitrix_robot_weather:handler_robot', but)
    except Exception as exc:
        return HttpResponse(str(exc))

    return HttpResponse('ok')
