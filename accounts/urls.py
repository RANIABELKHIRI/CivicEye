from django.urls import path
from .views import login, register, login_page, register_page, edit_profile, edit_profile_page
from . import views

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('api/profile/edit/', edit_profile),
  
     # 👇 لعرض الصفحة
    path('login-page/', login_page),
    path('register-page/', register_page),
    path('profile/edit/', edit_profile_page, name='edit-profile'),
   
]