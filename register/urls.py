from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from . import views


app_name = 'register'


urlpatterns = [
    path('login/', views.log_in, name='login'),
    path('logout/',LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.userprofile, name='profile'),
    path('edit-user-dashbord/', views.edit_user, name='edit_dashbord'),
    path('password-reset/', PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name="password_reset"),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),name="password_reset_confirm"),
    path('password-reset-done/', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),name="password_reset_done"),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),name="password_reset_complete"),
]
