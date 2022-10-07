from http import HTTPStatus
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import (DetailView, CreateView, DeleteView,
                                  ListView, TemplateView, UpdateView)
from requests import post
from users.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth import logout
from .models import  Publicacion
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from .forms import CrearPublicacionForm
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from .utils import is_ajax, DispatchAuthenticatedUserMixin, ValidateOwnershipMixin
from django.http import Http404




# VISTA PARA PERFIL DEL CREADOR DE CONTENIDO
class DetailCreador(DispatchAuthenticatedUserMixin, LoginRequiredMixin, ListView):
    model = Publicacion
    template_name = 'social/user/perfil.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        # Traemos el autor del perfil
        context['object'] = User.objects.get(slug = self.kwargs['slug'])
        context['innercontent'] = 'main/user/content.html'
        user = User.objects.get(slug = self.kwargs['slug'])

        return context

    def get_queryset(self, **kwargs):
        try:
            # Si el usuario no existe
            user = User.objects.get(slug = self.kwargs['slug'])
        except:
            # retorna error 404
            raise Http404

        
        
        return Publicacion.objects.filter(user = user).order_by('-fecha_creacion')


    def get_template_names(self):
        
        return ['social/user/perfil.html']

    def dispatch(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        if slug.lower() in ['marketplace', 'home']:

            if slug.lower() == 'home':

                return redirect(reverse('home-social'))

        return super().dispatch(request, *args, **kwargs)
        




# CRUD PUBLICACIONES

# Crear publicacion
class CrearPublicacionView(DispatchAuthenticatedUserMixin, LoginRequiredMixin, 
                            SuccessMessageMixin, CreateView):
    model = Publicacion
    template_name = 'social/user/crear-publi.html'
    form_class = CrearPublicacionForm
    success_message = 'La publicacion fue creada satisfactoriamente!'

    # Se sobrescribe el form_valid para guardar el autor.
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        return redirect(self.get_success_url())

    def get_success_url(self) -> str:
        return reverse('detalle-publicacion', kwargs={'pk': self.object.pk, 'user_slug': self.object.user.slug})


# Detalle Publicacion
class DetallePublicacionView(DispatchAuthenticatedUserMixin, LoginRequiredMixin, DetailView):
    model = Publicacion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.kwargs['user_slug'] != self.get_object().user.slug:
            raise Http404 

        context['innercontent'] = 'main/user/content.html'

        return context


    def get_template_names(self):
            return ['social/user/detalle-publicacion.html']     


# Update Publicacion

class UpdatePublicacionView(ValidateOwnershipMixin, LoginRequiredMixin, UpdateView):
    model = Publicacion
    fields = ['descripcion']
    template_name = 'social/user/update-publicacion.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.kwargs['user_slug'] != self.get_object().user.slug:
            raise Http404 

        context['innercontent'] = 'main/user/content.html'

        return context




# Delete Publicacion
class DeletePublicacionView(ValidateOwnershipMixin, LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Publicacion
    success_url = reverse_lazy('social-home')
    success_message = 'Publicacion eliminada con exito!'

    def get(self, *args, **kwargs):
        user_slug = self.kwargs['user_slug']
        pk = self.kwargs['pk']
        return redirect('detalle-publicacion', user_slug= user_slug, pk = pk)





# Lista Home Publicaciones

class HomeSocialView(DispatchAuthenticatedUserMixin, LoginRequiredMixin, ListView):
    model = Publicacion
    paginate_by = 3

    def get_queryset(self):
        
        # Aca primero se deberia retornar las publicaciones de personas que sigue.
        # Si no sigue a nadie se buscarian por tipo de celebridad segun las mismas que tiene el.
        # En caso de no tener ningun tipo de celebridad entonces de las personas relevantes primero.
        # En orden de mas nuevo a mas antiguo.
        # Y de ultimo irian las publicaciones en general de personas de mas nuevo a mas antiguo.
       
        return Publicacion.objects.all().order_by('-fecha_creacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aca se traerian a las personas relevantes.
        # Y personas a las cuales uno esta suscrito.

        context['innercontent'] = 'main/user/content.html'

        return context

    def get_template_names(self):

        return ['social/user/home-social.html']


class Likes(View):
    pass




