from django.shortcuts import render, redirect
from django.views.generic import DetailView, CreateView
from users.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
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

class CrearPublicacionView(LoginRequiredMixin, CreateView):
    model = Publicacion
    template_name = 'social/creador/crear-publi.html'
    fields = ['titulo', 'archivo', 'descripcion']

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.is_active:
                # Si el usuario es creador de contenido que lo deje entrar a la pagina.
                if self.request.user.groups.name == 'Creador de Contenido':
                    # Lo envia a crear la publicacion
                    return super().dispatch(request, *args, **kwargs)
                
                # Si no que retorne 404
                else:
                    return HttpResponseNotFound('Page not found.')

            else:
                logout(self.request)
                return redirect(reverse('account_inactive'))
        else:
            return redirect(reverse('account_login'))

    # Se sobrescribe el form_valid para guardar el autor.
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        return redirect(self.get_success_url())

    def get_success_url(self) -> str:
        return reverse('detalle-publicacion', kwargs={'pk': self.object.pk, 'user_slug': self.object.user.slug})


class DetallePublicacionView(LoginRequiredMixin, DetailView):
    model = Publicacion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_slug'] = self.get_object().user.slug

        # Si el tipo de usuario es creador de contenido retornar el template de el
        if self.request.user.groups.name == 'Creador de Contenido':
            context['innercontent'] = 'main/creador/content-creador.html'

        # Si no, contenido para consumidor
        else:
            context['innercontent'] = 'main/consumidor/content-consumidor.html'

        return context


    def get_template_names(self):
        if self.request.user.groups.name == 'Creador de Contenido':
            return ['social/creador/detalle-publicacion-creador.html']
        else:
            return ['social/consumidor/detalle-publicacion-consumidor.html']
            

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.is_active:
                # Si el usuario es consumidor o es el dueno del perfil
                if self.request.user.groups.name == 'Consumidor' or self.request.user == self.get_object().user:
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
