# Users views.py

from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login-page"),
    path('logout/', views.logoutPage, name="logout-page"),
    path('register/', views.registerPage, name="register-page"),
    path('profile/', views.userPage, name='user-page-redirect'),
    path('profile/<str:user_name>/', views.userPage, name="profile-page"),
    path('naughty-user/', views.naughty_user, name='naughty-page'),
]