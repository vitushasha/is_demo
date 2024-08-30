from django.urls import path
from .views.views import start_convert

app_name = 'convert_an_audio_to_text'

urlpatterns = [
    path('', start_convert, name='start_convert')
]