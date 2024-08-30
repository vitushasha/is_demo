from django.urls import path
from .views import views

app_name = 'supervisorsfinder'

urlpatterns = [
    path('', views.main_find, name='search')
]