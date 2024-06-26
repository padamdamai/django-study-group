from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login_page,name='login_page'),
    path('logout/',views.logout_page,name='logout_page'),
    path('register/',views.register_user,name='register'),
    path('',views.home,name="home"),
    path('room/<str:pk>/',views.room,name="room"),
    path('userProfile/<str:pk>/',views.userProfile,name="userProfile"),
    path('create-room/',views.createRoom,name='create-room'),
    path('update-room/<str:pk>/',views.updateRoom,name='update-room'),
    path('delete-room/<str:pk>/',views.deleteRoom,name='delete-room'),
    path('deleteMessage/<str:pk>/',views.deleteMessage,name='deleteMessage'),

    path('update-user',views.updateUser,name='update-user'),
    path('topicPage',views.topicPage,name='topicPage'),
    path('activityPage',views.activityPage,name='activityPage'),




 
]