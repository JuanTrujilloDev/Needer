"""
users URLS
"""
from django.urls import path, include
from django.views.defaults import page_not_found
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('social/signup/', SocialUserSignupView.as_view(), name="socialaccount_signup"),
    path('signup/', UserSignupView.as_view(), name="account_signup"),
    path('password/set', page_not_found, {'exception': Exception('Not Found')}, name="account_set_password"),
    path('logout/', LogoutView.as_view(), name="account_logout"),
    path('', include('allauth.urls')),
]
