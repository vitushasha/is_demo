from django.urls import path
from .views import export_to_powerbi, information_about_app

app_name = "download_deals"

urlpatterns = [
    path('', information_about_app.entrance, name='information'),
    path('export_deal/', export_to_powerbi.download_deals, name='export'),
]