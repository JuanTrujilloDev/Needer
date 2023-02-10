from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from main.utils import ExtendsInnerContentMixin

# Create your views here.
from chat.models import Thread



class ThreadListView (ExtendsInnerContentMixin, LoginRequiredMixin, ListView):
    model = Thread
    paginate_by = 10
    template_name = 'chat/messages.html'


    def get_queryset(self):
        return Thread.objects.by_user(user= self.request.user).order_by('-timestamp')


class ThreadDetailView (ExtendsInnerContentMixin, LoginRequiredMixin, DetailView):

    model = Thread
    template_name = 'chat/thread.html'
