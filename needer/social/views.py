from django.shortcuts import render, redirect
from django.views.generic import DetailView, CreateView
from users.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth import logout
from .models import Publicacion
from django.http import HttpResponseNotFound




# VISTA PARA PERFIL DEL CREADOR DE CONTENIDO
class DetailCreador(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'social/perfil-creador.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publicaciones'] = Publicacion.objects.filter(user = self.object).order_by('-fecha_creacion')


        # Si el tipo de usuario es creador de contenido retornar el template de el
        if self.request.user.groups.name == 'Creador de Contenido':
            context['innercontent'] = 'main/creador/content-creador.html'
        else:
            context['innercontent'] = 'main/consumidor/content-consumidor.html'

        return context


    def get_template_names(self):
        if self.request.user.groups.name == 'Creador de Contenido':
            return ['social/creador/perfil-solo-creador.html']
        else:
            return ['social/consumidor/perfil-creador-consumidor.html']
            

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.is_active:
                # Si el usuario es consumidor o es el dueno del perfil
                if self.request.user.groups.name == 'Consumidor' or self.request.user == self.get_object():
                    return super().dispatch(request, *args, **kwargs)

                # Si es creador de contenido pero no es el dueno del perfil
                elif self.request.user.groups.name == 'Creador de Contenido':
                    # Lo redirige a su perfil
                    return redirect(self.request.user.get_absolute_url())
                
                # Si no es ninguno que lo redirija a ERROR
                else:
                    return HttpResponseNotFound('Page not found.')

            else:
                logout(self.request)
                return redirect(reverse('account_inactive'))
        else:
            return redirect(reverse('account_login'))




# CRUD PUBLICACIONES

class CrearPublicacionView(CreateView):
    model = Publicacion

