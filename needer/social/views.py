from ast import Try
from http import HTTPStatus
import time
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import (DetailView, CreateView, DeleteView,
                                  ListView, TemplateView, UpdateView)
from requests import post
from users.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth import logout
from .models import LikedPublicacion, Publicacion
from django.http import JsonResponse,HttpResponse, HttpResponseNotFound, HttpResponseRedirect
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
        for i in list(context['object_list']):
            i.cant_Like = LikedPublicacion.objects.filter(id_publicacion =i.id).count()

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
        usuario = User.objects.get(id = self.request.user.id)

        like_find = LikedPublicacion.objects.filter(id_publicacion = kwargs['object'].id, id_usuario = usuario)
        if len(like_find)> 0: context['EstadoLike'] = True
        else :context['EstadoLike'] = False 
        cant_Like =LikedPublicacion.objects.filter(id_publicacion = kwargs['object'].id).count()
              
           
        if self.kwargs['user_slug'] != self.get_object().user.slug:
            raise Http404 

        context['CantLiked'] = cant_Like
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

        for i in list(context['object_list']):
            i.cant_Like = LikedPublicacion.objects.filter(id_publicacion =i.id).count()

        context['innercontent'] = 'main/user/content.html'
        return context

    def get_template_names(self):

        return ['social/user/home-social.html']


class AddLikes(LoginRequiredMixin, View):
    
    def post(self, request, pk, *args, **kwargs):
        self.publicacion = Publicacion.objects.get(id = pk)
        usuario = User.objects.get(id = request.user.id)
        cantidadlike = LikedPublicacion.objects.filter(id_publicacion = self.publicacion).count()
        """ Si el usuario ya dio like devuelva la cantidad de likes que tiene la publicacion """
        if LikedPublicacion.objects.filter(id_publicacion = self.publicacion, id_usuario =usuario).exists(): 
            cantidadlike = str(cantidadlike) + ' Me Gustas ' + '30 Comentarios'
            return JsonResponse({'result':cantidadlike})
        """ Si no ha dado like se crea el objeto y se suma + 1  """
        LikedPublicacion.objects.create(id_publicacion = self.publicacion, id_usuario =usuario)
        cantidadlike += 1
        cantidadlike = str(cantidadlike) + ' Me Gustas ' + '30 Comentarios'
        return JsonResponse({'result': cantidadlike})

    def get_success_url(self) -> str:
        return reverse('detalle-publicacion', kwargs={'pk': self.publicacion.id, 'user_slug': self.publicacion.user.slug})


class RemoveLikes(LoginRequiredMixin, View):
    
    def post(self, request, pk, *args, **kwargs):
        """ la pk es el id de la publicacion para obtener el objeto """
        self.publicacion = Publicacion.objects.get(id = pk)
        """ Se obtiene el usuario que da el no me gusta """
        usuario = User.objects.get(id = request.user.id)
        LikedPublicacion.objects.filter(id_publicacion = self.publicacion, id_usuario =usuario).delete()
        cantidadlike = len(LikedPublicacion.objects.filter(id_publicacion = self.publicacion))
        cantidadlike = str(cantidadlike) + ' Me Gustas ' + '30 Comentarios'
        return JsonResponse({'result': cantidadlike} )

    def get_success_url(self) -> str:
        return reverse('detalle-publicacion', kwargs={'pk': self.publicacion.id, 'user_slug': self.publicacion.user.slug})



