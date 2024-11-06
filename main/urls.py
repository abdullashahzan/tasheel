from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),

    path('', views.index, name='home'),
    path('services/', views.services, name='services'),
    path('modify_road/<str:option>/', views.modify_road, name='modify_road'),
    path('tell_crowd/', views.tell_crowd, name='tell_crowd'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('change_camera/', views.change_camera, name='change_camera'),
]