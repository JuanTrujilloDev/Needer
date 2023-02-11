from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from main.utils import ExtendsInnerContentMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.db.models import Q

# Create your views here.
from chat.models import Thread, ChatMessage



class ThreadListView (ExtendsInnerContentMixin, LoginRequiredMixin, ListView):
    model = Thread
    paginate_by = 20
    template_name = 'chat/messages.html'


    def get_queryset(self):
        return Thread.objects.by_user(user= self.request.user).order_by('-timestamp')


# TODO VISTA PARA BORRAR LOS THREADS


# TODO VISTA PARA AGREGAR NUEVO THREAD



class ThreadFilterView (ExtendsInnerContentMixin, LoginRequiredMixin, ListView):
    model = Thread
    paginate_by = 20
    template_name = 'chat/filter.html'

    def get_queryset(self):
        q = self.request.GET.get('q').strip()
        if len(q) == 0:
            return None
            
        return Thread.objects.filter((Q(first_person= self.request.user) & (Q(second_person__username__icontains = q) | Q(second_person__first_name__icontains= q) 
                                                                            | Q(second_person__first_name__icontains = q))) 
                                   | (Q(second_person = self.request.user) & (Q(first_person__username__icontains = q) | Q(first_person__first_name__icontains= q) 
                                                                            | Q(first_person__first_name__icontains = q))) | 
                                     ((Q(first_person= self.request.user) | Q(second_person = self.request.user)) & 
                                       Q(chatmessage_thread__message__icontains=q))).order_by('-timestamp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context

    



# TODO meterle seguridad a los chats
# LIST VIEW
class ThreadDetailView (ExtendsInnerContentMixin, LoginRequiredMixin, DetailView):

    # Paginate by 20
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


