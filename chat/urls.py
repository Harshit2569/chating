from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.set_username, name='set_username'),
    path('rooms/', views.index, name='index'),
    path('room/<int:room_id>/', views.room, name='room'),
    path('create/', views.create_room, name='create_room'),
    path('logout/', views.logout_user, name='logout_user'),
]
