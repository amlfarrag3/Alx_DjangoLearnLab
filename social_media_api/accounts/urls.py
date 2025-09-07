# accounts/urls.py
from django.urls import path
from .views import UserRegistrationView, CustomAuthToken, UserProfileView
from .views import Follow_User, Unfollow_User

urlpatterns = [
    # URL for user registration
    path('register/', UserRegistrationView.as_view(), name='user-registration'),

    # URL for login (authentication via token)
    path('login/', CustomAuthToken.as_view(), name='token-login'),

    # URL for user profile (to be implemented)
    path('profile/', UserProfileView.as_view(), name='user-profile'),

    # URL for following a user
    path('follow/<int:pk>/', Follow_User.as_view(), name='follow-user'),

    # URL for unfollowing a user
    path('unfollow/<int:pk>/', Unfollow_User.as_view(), name='unfollow-user'),
]   

["unfollow/<int:user_id>/", "follow/<int:user_id>"]