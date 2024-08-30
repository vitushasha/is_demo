from django.urls import path
from .views import views


app_name = 'products_finder'


urlpatterns = [
    path('', views.products_finder, name='search'),
]