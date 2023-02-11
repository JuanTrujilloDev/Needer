from django.urls import path
from .views import *

urlpatterns = [
    path('chat/', ThreadListView .as_view(), name='chat'),
    path('chat/<int:pk>/', ThreadDetailView.as_view(), name='thread'),
    path('chat/filter/', ThreadFilterView.as_view(), name='thread-filter')
]
