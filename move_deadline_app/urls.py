from django.urls import path
from .views import views, move_deadline_of_task

app_name = 'move_deadline_app'

urlpatterns = [
    path('face_page/', views.face_page, name='face_page'),
    path('bind_handler/', views.bind_handler, name='bind_handler'),
    path('unbind_handler/', views.unbind_handler, name='unbind_handler'),
    path('page_with_button/', move_deadline_of_task.page_with_button, name='page_with_button'),
    path('move_function/', move_deadline_of_task.move_function, name='move_function'),
]