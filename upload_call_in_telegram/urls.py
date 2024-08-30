from django.urls import path
from .views.export import export_calls
from .views.keep_syn import keep_synced
from .views.pull_flag import get_flag
from .views.put_flag import set_flag

app_name = 'upload_call_in_telegram'

urlpatterns = [
    path('send_call_info/', export_calls, name='export'),
    path('keep_synced/', keep_synced, name='keep_syn'),
    path('get_flag/', get_flag, name='get_call_sync_flag'),
    path('set_flag/', set_flag, name='set_call_sync_flag'),
]