from django.http import HttpResponse

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from robot_weather_app.models.robot_model import RobotWeatherModel


@main_auth(on_cookies=True)
def uninstall(request):
    try:
        RobotWeatherModel.uninstall(request.bitrix_user_token)
    except Exception as exc:
        return HttpResponse(str(exc))

    return HttpResponse('ok')
