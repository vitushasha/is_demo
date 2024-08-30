from django.urls import path
from .views import views

app_name = 'sort_companies'

urlpatterns = [
    path('', views.sort_companies, name='sort')
]