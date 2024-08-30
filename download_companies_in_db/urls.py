from django.urls import path
from download_companies_in_db.views.sync_companies import sync_companies
from download_companies_in_db.views.launch_page import launch_page

app_name = 'download_companies_in_db'

urlpatterns = [
    path('', launch_page, name='home_page'),
    path('download_companies/', sync_companies, name='sync_companies'),
]