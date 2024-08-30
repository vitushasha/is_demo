from django.urls import path

from .views import views

app_name = 'bestcallmanager'

urlpatterns = [
    path('create_tasks/', views.create_tasks,
         name='create_tasks'),
    path('show_best_calls/', views.show_best_calls,
         name='show_best_calls'),
]