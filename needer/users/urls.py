"""
users URLS
"""
from django.urls import path, include
from django.views.defaults import page_not_found

urlpatterns = [
    path('email/', page_not_found, {'exception': Exception('Not Found')}, name="account_email"),
    path('password/set', page_not_found, {'exception': Exception('Not Found')}, name="account_set_password"),
    path('', include('allauth.urls')),
]
