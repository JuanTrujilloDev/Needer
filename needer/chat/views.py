from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from main.utils import ExtendsInnerContentMixin
from django.shortcuts import redirect
from django.urls import reverse

# Create your views here.
from chat.models import Thread, ChatMessage



class ThreadListView (ExtendsInnerContentMixin, LoginRequiredMixin, ListView):
    model = Thread
    paginate_by = 10
    template_name = 'chat/messages.html'


    def get_queryset(self):
        return Thread.objects.by_user(user= self.request.user).order_by('-timestamp')


# TODO meterle seguridad a los chats
class ThreadDetailView (ExtendsInnerContentMixin, LoginRequiredMixin, DetailView):

    model = Thread
    template_name = 'chat/thread.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['me'] = self.request.user
        context['thread'] = Thread.objects.get(id = self.kwargs['pk'])

        if self.request.user ==  context['thread'].first_person:
            context['user'] =  context['thread'].second_person

        else:
            context['user'] =  context['thread'].first_person

        context['messages'] = ChatMessage.objects.filter(thread= context['thread'])

        return context
    

    def get(self, request, **kwargs):
        thread = Thread.objects.get(id = self.kwargs['pk'])

        print(thread.second_person.username)
        if self.request.user ==  thread.first_person or self.request.user ==  thread.second_person:

            return render(request, self.template_name, kwargs)

        else:
            return redirect(reverse('chat'))


    #POST AJAX 