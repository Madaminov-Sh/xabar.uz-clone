from django.urls import path

from register.api_view import apiviews

urlpatterns = [
    path('users/', apiviews.UsersAPIView.as_view()),
    path('register/', apiviews.RegisterAPIView.as_view()),
    path('login/', apiviews.LoginAPIView.as_view()),
    path('logout/', apiviews.LogoutAPIView.as_view()),
    path('forgot/password/', apiviews.ForgotPasswordAPIView.as_view()),

    path('profiles/', apiviews.ProfileListsAPIView.as_view()),
    path('profile/<int:pk>/', apiviews.UserProfileAPIView.as_view()),
    path('profile/<int:id>/posts/', apiviews.UserProfilePostsAPIView.as_view()),
    path('profile/<int:pk>/edit/', apiviews.ProfileEditAPIView.as_view()),

]



