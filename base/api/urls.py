from django.urls import path 
from . import views

urlpatterns = [
    path('',views.getRoutes),
    path('rooms/',views.getRoooms),
    path('rooms/<str:pk>/',views.getRooom),

]