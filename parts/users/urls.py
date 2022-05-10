# Users views.py

from django.urls import path, include

from .forms import UserPasswordChangeForm, UserPasswordResetForm
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.loginPage, name="login-page"),
    path('logout/', views.logoutPage, name="logout-page"),
    path('register/', views.registerPage, name="register-page"),
    path('profile/', views.userPage, name='user-page-redirect'),
    path('profile/<str:user_name>/', views.userPage, name="profile-page"),
    path('naughty-user/', views.naughty_user, name='naughty-page'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name="base/password-reset.html", html_email_template_name='base/password-reset-email.html', form_class=UserPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="base/password-reset-done.html"), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="base/password-reset-form.html", form_class=UserPasswordChangeForm), name='password_reset_confirm'),
    path('password-reset-complete/', views.passwordComplete, name='password_reset_complete'),
    path('reset-username-check/', views.resetUsernameCheck, name='reset-username-check'),

    path('contact-us/', views.contact_admin, name='contact-us'),
    path('active-contact-submissions/<str:msg_type>/', views.active_contact_submissions, name='active-contact-submissions'),
    path('active-contact-review/<int:contact_id>/', views.active_contact_review, name='active-contact-review'),


]