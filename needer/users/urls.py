"""
users URLS
"""
from django.urls import path, include
from django.views.defaults import page_not_found
from allauth.account.views import PasswordResetView
from .views import *
from django.contrib.auth.views import LogoutView
from .forms import CustomResetPasswordForm

urlpatterns = [
    path('social/signup/', SocialUserSignupView.as_view(), name="socialaccount_signup"),
    path('signup/', UserSignupView.as_view(), name="account_signup"),
    path('password/set', page_not_found, {'exception': Exception('Not Found')}, name="account_set_password"),
    path('logout/', LogoutView.as_view(), name="account_logout"),
    path('password/reset/', PasswordResetView.as_view(form_class = CustomResetPasswordForm), name="account_reset_password"),
    path('profile/', updateAccountViewResolver, name='account_profile'),
    path('', include('allauth.urls')),
    
]
