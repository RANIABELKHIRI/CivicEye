from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='index'),

    path('citizen/home/', views.citizen_home , name='citizen-home'),
    path('service1/home/', views.service1_home),
    path('service2/home/', views.service2_home),
    path('service3/home/', views.service3_home),
    path('authorities/', views.authorities_home, name='authorities'),

]
