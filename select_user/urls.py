from django.urls import path
from .views.select_user import select_user

urlpatterns = [
    path('', select_user, name='select_user')
]