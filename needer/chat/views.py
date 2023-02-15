from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from main.utils import ExtendsInnerContentMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.db.models import Q
from users.models import User
import urllib
from django.contrib import messages
from .forms import ThreadForm
from django.utils.safestring import mark_safe
from social.utils import PreventGetMethodMixin
from django.core.exceptions import PermissionDenied
from django.utils import timezone

# Create your views here.
from chat.models import Thread, ChatMessage



class ThreadListView (ExtendsInnerContentMixin, LoginRequiredMixin, ListView):
    model = Thread
    paginate_by = 20
    template_name = 'chat/messages.html'

    # TODO Listar solo los elementos que el timestamp es mayor a closed by
    # TODO Traer threads que solo tengan mensajes


    def get_queryset(self):
        threads = Thread.objects.by_user(user= self.request.user).order_by('-updated')
        thread_list = []
        user = self.request.user

        for thread in threads:
            print(thread.closed_by_first_user , thread.closed_by_second_user, thread.updated)
            if thread.first_person == user:
                if thread.closed_by_first_user <= thread.updated: thread_list.append(thread)
            elif thread.second_person == user:
                if thread.closed_by_second_user <= thread.updated: thread_list.append(thread)
            else: pass
       
        return thread_list


# TODO VISTA PARA BORRAR LOS THREADS
# PREVENT GET METHOD
class ThreadDeleteView(PreventGetMethodMixin, LoginRequiredMixin, UpdateView):
    # Si closed_by tal user es menor a timestamp al usuario le aparecerian los mensajes despues del timestamp.
    # Si ambos son mayores al timestamp se eliminan todos los mensajes y el thread.
    # TODO en los mensajes solo traer dependiento del closed_by y timestamp
    # TODO en el filterview si el objeto existe, si que lo traiga

    model = Thread
    fields = ['closed_by_first_user', 'closed_by_second_user']
    template_name = 'chat/messages.html'
    
    def post(self,request, **kwargs):
        self.object = self.get_object()
        
        if self.request.user == self.object.first_person or self.request.user == self.object.second_person:

            if self.request.user == self.object.first_person: 
                self.object.closed_by_first_user = timezone.now()
            else:
                self.object.closed_by_second_user = timezone.now()

            self.object.save()

            if self.object.closed_by_first_user > self.object.updated and self.object.closed_by_second_user > self.object.updated:
                ChatMessage.objects.filter(thread__id = self.object.id).delete()
            
                
            messages.success(request, 'Se ha eliminado el chat correctamente')
            return redirect(reverse('chat'))

        raise PermissionDenied


# VISTA PARA AGREGAR NUEVO THREAD
class ThreadCreateView(ExtendsInnerContentMixin, LoginRequiredMixin, CreateView):
    model = Thread
    form_class = ThreadForm
    template_name  = 'chat/thread-crear.html'

    def form_valid(self, form):

        cleaned_data = form.cleaned_data
        user = cleaned_data['second_person']
        thread = Thread.objects.filter((Q(first_person = user) & (Q(second_person = self.request.user))) | (Q(first_person = self.request.user) & (Q(second_person = user))))
        if thread:
            # AGREGAR LINK PARA IR AL DETALLE
            link_filtrar = reverse('chat')
            messages.add_message(self.request, 40, mark_safe(f'Error, ya hay un chat con esta persona <a href="{thread[0].get_absolute_url()}">AQUI</a>. Si no lo encuentras, <a href="{link_filtrar}"> filtralo entre tus chats </a>'))
            return super().form_invalid(form)

        self.object = form.save(commit = False)
        self.object.first_person = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self, **kwargs) -> str:
        return reverse('thread', kwargs={'pk':self.object.pk})
        



        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seguidores = self.request.user.get_user_followers()
        seguidos = self.request.user.get_user_followed()
        users = list(dict.fromkeys(seguidores + seguidos))
       
        all_users = User.objects.all().exclude(id=self.request.user.id)
        all_users = [ user for user in all_users.exclude(pk__in=[user.pk  for user in users])]
       
        context['users'] = users + all_users

        return context


class ThreadFilterView (ExtendsInnerContentMixin, LoginRequiredMixin, ListView):
    model = Thread
    paginate_by = 20
    template_name = 'chat/filter.html'


    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # Trae el query a realizar
        query = self.request.GET.get('q')
        
        # Si no trae el query retornar directamente el context_data
        if not query:
            
            return context_data
        
        # Traducir el query url a formato entendible
        query = urllib.parse.unquote(query)
        query = query.lower()
        special_characters = '"!@#$%^&*()-+?_=,<>/"'
        
        # No permitir caracteres especiales
        if any(c in special_characters for c in query) or len(query.replace(" ", "")) < 1:
          messages.add_message(self.request, 40, 'Error en la busqueda.')
          return context_data
          # En caso de haber caracteres especiales en el get_queryset arroja error.
          # messages.error(self.request, 'No se permiten caracteres especiales en la busqueda.')

        else: 
            # En caso contrario trae los objetos
            #TODO ORDERNAR POR NUMERO DE SEGUIDORES
            query = query.strip()
        
            #TODO FILTRAR PRODUCTOS
            # context_data['productos'] 
        context_data['q'] = query
        return context_data


    def get_queryset(self):
        """Devuelve todos los objetos de la consulta de filtrado
        q: parametro de consulta


        Returns:
            object: objetos que contene el parametro q
        """ 
        
        #.split() se usa para cuando se pasa un parametro de solo espacio pueda ser evaluado
        # ' ', segundo parametro de get es para evitar errores en la consulta en caso de que no se pasen parametros 

        q = self.request.GET.get('q')

        if q:

           
            q = urllib.parse.unquote(q.lower())
            q = q.lower()
            special_characters = '"!@#$%^&*()-+?_=,<>/"'

            # Si la busqueda son solo espacios arrojaria error
            if len(q.replace(" ", "")) < 1:
                messages.add_message(self.request, 40, 'Busqueda vacia.')
                return []

            # Si tiene contenido
            else:
                # No permitir caracteres especiales
                if any(c in special_characters for c in q):
                    messages.add_message(self.request, 40, 'No se permiten caracteres especiales en la busqueda.')
                    return []
                else: 
                    return Thread.objects.filter((Q(first_person= self.request.user) & (Q(second_person__username__icontains = q) | Q(second_person__first_name__icontains= q) 
                                                                            | Q(second_person__first_name__icontains = q))) 
                                   | (Q(second_person = self.request.user) & (Q(first_person__username__icontains = q) | Q(first_person__first_name__icontains= q) 
                                                                            | Q(first_person__first_name__icontains = q))) 
                                    ).order_by('-updated') 
                    

        else:
            
            return []

                                    
    

    



# TODO meterle seguridad a los chats
# LIST VIEW
class ThreadDetailView (ExtendsInnerContentMixin, LoginRequiredMixin, DetailView):
    # TODO Filtro segun el closed_by
    model = Thread
    template_name = 'chat/thread.html'

    def dispatch(self, request, *args, **kwargs):
        thread = get_object_or_404(Thread, id=self.kwargs['pk'])
        if self.request.user == thread.first_person or self.request.user == thread.second_person:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect(reverse('chat'))



    



