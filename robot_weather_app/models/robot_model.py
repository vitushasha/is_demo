from integration_utils.bitrix_robots.models import BaseRobot
import requests as req


class RobotWeatherModel(BaseRobot):

    CODE = 'robot_weather_app'
    NAME = 'Робот, возвращающий актуальные данные о погоде'
    USE_SUBSCRIPTION = True


    PROPERTIES = {
        'user': {
            'Name': {'ru': 'Получатель'},
            'Value': {'ru': 'Ответственный'},
            'Type': 'user',
            'Required': 'Y',
        },
        'city_name': {
            'Name': {'ru': 'Город'},
            'Type': 'string',
            'Required': 'Y'
        }
    }

    RETURN_PROPERTIES = {
        'city_name': {
            'Name': {'ru': 'Город'},
            'Type': 'string',
            'Required': 'Y'
        },
        'time': {
            'Name': {'ru': 'Время'},
            'Type': 'string',
            'Required': 'Y'
        },
        'temperature': {
            'Name': {'ru': 'Температура'},
            'Type': 'int',
            'Required': 'Y'
        },
        'weather_description': {
            'Name': {'ru': 'Описание'},
            'Type': 'string',
            'Required': 'Y'
        },
        'wind_speed': {
            'Name': {'ru': 'Скорость ветра'},
            'Type': 'int',
            'Required': 'Y'
        },
        'wind_degree': {
            'Name': {'ru': 'Угол ветра'},
            'Type': 'int',
            'Required': 'Y'
        },
        'wind_dir': {
            'Name': {'ru': 'Направление ветра'},
            'Type': 'string',
            'Required': 'Y'
        },
        'pressure': {
            'Name': {'ru': 'Атмосферное давление'},
            'Type': 'int',
            'Required': 'Y'
        },
        'humidity': {
            'Name': {'ru': 'Влажность воздуха'},
            'Type': 'int',
            'Required': 'Y'
        },
        'precip': {
            'Name': {'ru': 'Осдаки (мм)'},
            'Type': 'int',
            'Required': 'Y'
        },
        'cloudcover': {
            'Name': {'ru': 'Облачность'},
            'Type': 'int',
            'Required': 'Y'
        },
        'feelslike': {
            'Name': {'ru': 'Температура ощущается как'},
            'Type': 'int',
            'Required': 'Y'
        },
        'visibility': {
            'Name': {'ru': 'Видимость'},
            'Type': 'int',
            'Required': 'Y'
        },
        'ok': {
            'Name': {'ru': 'ok'},
            'Type': 'bool',
            'Required': 'Y',
        },
        'error': {
            'Name': {'ru': 'error'},
            'Type': 'string',
            'Required': 'N',
        },
    }


    def process(self) -> dict:
        try:
            response = req.get(f'https://api.weatherstack.com/current?access_key=e4cb022f31c56f736d1bfcde5f3210e9&query=Moscow')
            data = response.json()
            weather = data['current']
            self.dynamic_token.call_api_method('bizproc.event.send', {"event_token": self.event_token,
                                                                      "return_values": {'city_name': data['location']['name'],
                                                                                        # Время
                                                                                        'time': weather['time'],
                                                                                        # Температупа
                                                                                        'temperature': weather['temperature'],
                                                                                        # Описание погоды
                                                                                        'weather_description': weather['weather_description'][0],
                                                                                        # Скорость ветра
                                                                                        'wind_speed': weather['wind_speed'],
                                                                                        # Угол ветра
                                                                                        'wind_degree': weather['wind_degree'],
                                                                                        # Направление ветра
                                                                                        'wind_dir': weather['wind_dir'],
                                                                                        # Атмосферное давление
                                                                                        'pressure': weather['pressure'],
                                                                                        # Влажность
                                                                                        'humidity': weather['humidity'],
                                                                                        # Осадки
                                                                                        'precip': weather['precip'],
                                                                                        # Облачность
                                                                                        'cloudcover': weather['cloudcover'],
                                                                                        # Чувствительность
                                                                                        'feelslike': weather['feelslike'],
                                                                                        # Видимость
                                                                                        'visibility': weather['visibility']}})

        except KeyError:
            self.dynamic_token.call_api_method('bizproc.event.send', {"event_token": self.event_token,
                                                                      "return_values": {'city_name': 'Что-то пошло не так',
                                                                                        # Время
                                                                                        'time': 'Что-то пошло не так',
                                                                                        # Температупа
                                                                                        'temperature': '',
                                                                                        # Описание погоды
                                                                                        'weather_description': 'Что-то пошло не так',
                                                                                        # Скорость ветра
                                                                                        'wind_speed': '',
                                                                                        # Угол ветра
                                                                                        'wind_degree': '',
                                                                                        # Направление ветра
                                                                                        'wind_dir': 'Что-то пошло не так',
                                                                                        # Атмосферное давление
                                                                                        'pressure': '',
                                                                                        # Влажность
                                                                                        'humidity': '',
                                                                                        # Осадки
                                                                                        'precip': '',
                                                                                        # Облачность
                                                                                        'cloudcover': '',
                                                                                        # Чувствительность
                                                                                        'feelslike': '',
                                                                                        # Видимость
                                                                                        'visibility': ''}})

        except Exception as exc:
            return dict(ok=False, error=str(exc))

        return dict(ok=True)
                                                                                        # Температупа
                                                                                        #'temperature': '',
                                                                                        # Описание погоды
                                                                                        #'weather_description': 'Что-то пошло не так',
                                                                                        # Скорость ветра
                                                                                        #'wind_speed': '',
                                                                                        # Угол ветра
                                                                                        #'wind_degree': '',
                                                                                        # Направление ветра
                                                                                        #'wind_dir': 'Что-то пошло не так',
                                                                                        # Атмосферное давление
                                                                                        #'pressure': '',
                                                                                        # Влажность
                                                                                        #'humidity': '',
                                                                                        # Осадки
                                                                                        #'precip': '',
                                                                                        # Облачность
                                                                                        #'cloudcover': '',
                                                                                        # Чувствительность
                                                                                        #'feelslike': '',
                                                                                        # Видимость
                                                                                        #'visibility': ''}})

"""'temperature': {
            'Name': {'ru': 'Температура'},
            'Type': 'string',
            'Required': 'Y'
        },
        'weather_description': {
            'Name': {'ru': 'Описание'},
            'Type': 'string',
            'Required': 'Y'
        },
        'wind_speed': {
            'Name': {'ru': 'Скорость ветра'},
            'Type': 'string',
            'Required': 'Y'
        },
        'wind_degree': {
            'Name': {'ru': 'Угол ветра'},
            'Type': 'string',
            'Required': 'Y'
        },
        'wind_dir': {
            'Name': {'ru': 'Направление ветра'},
            'Type': 'string',
            'Required': 'Y'
        },
        'pressure': {
            'Name': {'ru': 'Атмосферное давление'},
            'Type': 'string',
            'Required': 'Y'
        },
        'humidity': {
            'Name': {'ru': 'Влажность воздуха'},
            'Type': 'string',
            'Required': 'Y'
        },
        'precip': {
            'Name': {'ru': 'Осдаки (мм)'},
            'Type': 'string',
            'Required': 'Y'
        },
        'cloudcover': {
            'Name': {'ru': 'Облачность'},
            'Type': 'string',
            'Required': 'Y'
        },
        'feelslike': {
            'Name': {'ru': 'Температура ощущается как'},
            'Type': 'string',
            'Required': 'Y'
        },
        'visibility': {
            'Name': {'ru': 'Видимость'},
            'Type': 'string',
            'Required': 'Y'
        },
        'ok': {
            'Name': {'ru': 'ok'},
            'Type': 'bool',
            'Required': 'Y',
        },
        'error': {
            'Name': {'ru': 'error'},
            'Type': 'string',
            'Required': 'N',
        },
"""

