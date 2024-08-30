from django.urls import path
from .views import views

app_name = 'call_register'

urlpatterns = [
    path('reg_call/', views.reg_call, name='reg_call')
]