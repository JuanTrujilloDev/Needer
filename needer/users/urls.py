"""
users URLS
"""
from django.urls import path, include
from django.views.defaults import page_not_found
from .views import *

urlpatterns = [
    path('password/set', page_not_found, {'exception': Exception('Not Found')}, name="account_set_password"),
    path('', include('allauth.urls')),
]
