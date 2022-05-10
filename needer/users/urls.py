"""
users URLS
"""
from django.urls import path, include
from django.views.defaults import page_not_found
from .views import *

urlpatterns = [
    path('email/', page_not_found, {'exception': Exception('Not Found')}, name="account_email"),
    path('password/set', page_not_found, {'exception': Exception('Not Found')}, name="account_set_password"),
    path('social/signup/', SocialUserSignupView.as_view(), name="socialaccount_signup"),
    path('signup/', UserSignupView.as_view(), name="signup"),
    path('', include('allauth.urls')),
]
