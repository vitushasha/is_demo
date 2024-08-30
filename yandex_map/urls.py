from django.urls import path
from .views.get_companies import get_companies
from .views.main_page import index

urlpatterns = [
    path('', index, name='index'),
    path('get_companies/', get_companies, name='get_companies')
]