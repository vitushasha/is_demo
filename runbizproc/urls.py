from django.urls import path
from .views.views import run_bizproc

app_name = 'runbizproc'

urlpatterns = [
    path('', run_bizproc, name='run')
]