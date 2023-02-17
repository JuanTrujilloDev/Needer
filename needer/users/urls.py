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
    path('social/connections/', CustomConnectionsView.as_view(), name="socialaccount_connections"),
    path('signup/', UserSignupView.as_view(), name="account_signup"),
    path('password/set', page_not_found, {'exception': Exception('Not Found')}, name="account_set_password"),
    path('logout/', LogoutView.as_view(), name="account_logout"),
    path('email/', CustomEmailChangeView.as_view(), name="account_email"),
    path('password/reset/', PasswordResetView.as_view(form_class = CustomResetPasswordForm), name="account_reset_password"),
    path('password/change/', CustomPasswordChangeView.as_view(), name="account_change_password"),
    path('inactive/', CustomInactiveView.as_view(), name="account_inactive"),
    path('profile/', updateAccountViewResolver, name='account_profile'),
    path('delete-user/', UserDeleteView.as_view(), name='delete_user'),
    path('', include('allauth.urls')),



    
]
