from django.urls import path
from .views.views import load_from_googledocs

app_name = 'import_data'

urlpatterns = [
    path('', load_from_googledocs, name='load_from_googledocs')
]