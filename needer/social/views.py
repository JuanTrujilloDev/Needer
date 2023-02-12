import json
from multiprocessing import context, set_forkserver_preload
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import (DetailView, CreateView, DeleteView,
                                  ListView, TemplateView, UpdateView)
from requests import delete
from users.models import User, SeguidorUsuario
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy

from .models import (Comentarios, LikeComentarios, LikedPublicacion, 
                     Publicacion)
from django.http import HttpResponse, JsonResponse
from .forms import CrearComentarios, CrearPublicacionForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .utils import *
from django.http import Http404
from django.db.models import Q
import re
import urllib
from main.utils import *



# VISTA PARA PERFIL DEL CREADOR DE CONTENIDO
class DetailCreador(DispatchAuthenticatedUserMixin, LoginRequiredMixin, ListView):
    model = Publicacion
    template_name = 'social/user/perfil.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        # Traemos el autor del perfil
        context['object'] = get_object_or_404(User, slug = self.kwargs['slug'])
        context['innercontent'] = 'main/user/content.html'
        user = get_object_or_404(User, slug = self.kwargs['slug'])
        context['seguidores'] = user.get_user_followers()
        context['seguidos'] = user.get_user_followed()
        return context



    def get_queryset(self, **kwargs):
        try:
            # Si el usuario no existe
            user = get_object_or_404(User, slug = self.kwargs['slug'])
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
class DetallePublicacionView(ExtendsInnerContentMixin, DispatchAuthenticatedUserMixin, LoginRequiredMixin, ListView):
    model = Comentarios
    paginate_by = 10
    ordering = ["-fecha_creacion"]


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Se trae la Publicacion a la vista
        autor = get_object_or_404(User, slug=self.kwargs['user_slug'])
        context["publicacion"] = Publicacion.objects.get(Q(user=autor) & Q(id=self.kwargs["pk"]))
        


        

        """ Evalua si el usuario ya dio like a la publicacion """
        like_find = LikedPublicacion.objects.filter(id_publicacion = context["publicacion"].id, user = self.request.user)
        if len(like_find)> 0: context['EstadoLike'] = True
        else :context['EstadoLike'] = False 
        
              
           
        if self.kwargs['user_slug'] != context["publicacion"].user.slug:
            raise Http404 

        context["publicacion"].bool_comment = Comentarios.objects.filter(Q(id_publicacion = context["publicacion"]) & Q(user = self.request.user)).exists()

        """ Se carga el formulario y se evalua en la vista de CrearComentarioView """
        context['form'] = CrearComentarios

        for i in list(context['object_list']):
            
            i.bool_like =LikeComentarios.objects.filter(id_comentario =i.id, user = self.request.user).exists()

        return context

    def get_queryset(self):
        autor = get_object_or_404(User, slug=self.kwargs['user_slug'])
        publicacion = get_object_or_404(Publicacion,Q(user=autor) & Q(id=self.kwargs["pk"]))
        return Comentarios.objects.filter(Q(id_publicacion=publicacion)).order_by("-fecha_creacion")

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

    success_message = 'Publicacion eliminada con exito!'

    def get(self, *args, **kwargs):
        user_slug = self.kwargs['user_slug']
        pk = self.kwargs['pk']
        return redirect('detalle-publicacion', user_slug= user_slug, pk = pk)
        
    def get_success_url(self) -> str:
        return reverse('detalle-creador', kwargs={'slug': self.get_object().user.slug })





# Lista Home Publicaciones

class HomeSocialView(ExtendsInnerContentMixin, DispatchAuthenticatedUserMixin, LoginRequiredMixin, ListView):
    model = Publicacion
    paginate_by = 5

    def get_queryset(self):
        
        # Aca primero se deberia retornar las publicaciones de personas que sigue.
        # Si no sigue a nadie se buscarian por tipo de celebridad segun las mismas que tiene el.
        # En caso de no tener ningun tipo de celebridad entonces de las personas relevantes primero.
        # En orden de mas nuevo a mas antiguo.
        # Y de ultimo irian las publicaciones en general de personas de mas nuevo a mas antiguo.
        seguidos = self.request.user.get_user_followed()
        seguidores = self.request.user.get_user_followers()
        
        if len(seguidores) != 0 or len(seguidos) != 0:
            publicaciones_followers = Publicacion.objects.order_by('-fecha_creacion').filter(Q(user__in=seguidos) | Q(user__in=seguidores))
            publicaciones = Publicacion.objects.all().exclude(user=self.request.user).order_by('-fecha_creacion')
            publicaciones = publicaciones.exclude(id__in= [publicacion.id for publicacion in publicaciones_followers])

            resultado = [ publicacion for publicacion in publicaciones_followers] + [ publicacion for publicacion in publicaciones]

            return resultado 

        return Publicacion.objects.all().exclude(user=self.request.user).order_by('-fecha_creacion') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        """ Asignacion de la cantidad de likes, comentarios y si el usuario le ha dado like
            a la publicacion o no le ha dado like """
        for i in list(context['object_list']):
            i.bool_like = LikedPublicacion.objects.filter(Q(id_publicacion =i.id) & Q(user = self.request.user)).exists()
            i.bool_comment = Comentarios.objects.filter(Q(id_publicacion =i.id) & Q(user = self.request.user)).exists()

        context['innercontent'] = 'main/user/content.html'
        return context

    def get_template_names(self):

        return ['social/user/home-social.html']

""" Crear Likes publicacion"""

class AddLikesPublicacion(PreventGetMethodMixin, LoginRequiredMixin, View):


    model = LikedPublicacion

    def get_queryset(self):
        self.queryset =  self.model.objects.filter(id_publicacion = self.publicacion)
        return self.queryset

    def post(self, request, pk, *args, **kwargs):
        self.publicacion = Publicacion.objects.get(id = pk)
        usuario = get_object_or_404(User, id = request.user.id)

        query = self.get_queryset()
        cantidadlike = self.publicacion.cantidadLikes()

        result = {}
        listado = []
        result['pk'] =  self.publicacion.id
        result['url'] =  self.publicacion.disPublicacion()

        """ Si el usuario ya dio like devuelva la cantidad de likes que tiene la publicacion """

        if query.filter(user = self.request.user).exists(): 
            result['likes'] =  str(cantidadlike)
            listado.append(result)
            listado = json.dumps(listado)
            return JsonResponse({'result': listado} )
        """ Si no ha dado like se crea el objeto y se suma + 1  """
        query.create(id_publicacion = self.publicacion, user =usuario)
        cantidadlike += 1
        result['likes'] =  str(cantidadlike)
        listado.append(result)
        listado = json.dumps(listado)
        return JsonResponse({'result': listado} )

    def get_success_url(self) -> str:
        return reverse('detalle-publicacion', kwargs={'pk': self.publicacion.id, 'user_slug': self.publicacion.user.slug})



""" Eliminar Likes publicacion"""

class RemoveLikesPublicacion(PreventGetMethodMixin, ValidateOwnershipMixin, LoginRequiredMixin, View):

    model = LikedPublicacion

    def get_queryset(self):
        self.publicacion = Publicacion.objects.get(id = self.kwargs["pk"])
        self.queryset =  self.model.objects.get(id_publicacion = self.publicacion, user =self.request.user)
        return self.queryset

    def get_object(self):
        return self.get_queryset()

    

    def post(self, request, pk, *args, **kwargs):
        """ la pk es el id de la publicacion para obtener el objeto """
        self.publicacion = Publicacion.objects.get(id = pk)
        """ Se obtiene el usuario que da el no me gusta """
        query = self.get_queryset()
        query.delete()
        cantidadlike = self.publicacion.cantidadLikes()
        result = {}
        listado = []
        result['pk'] =  self.publicacion.id
        result['likes'] =  str(cantidadlike)

        result['url'] =  self.publicacion.likePublicacion()
        listado.append(result)
        listado = json.dumps(listado)
        return JsonResponse({'result': listado} )

    def get_success_url(self) -> str:
        return reverse('detalle-publicacion', kwargs={'pk': self.publicacion.id, 'user_slug': self.publicacion.user.slug})


""" Crear Comentario """

class CrearComentarioView(DispatchAuthenticatedUserMixin,LoginRequiredMixin, CreateView):

    model = Comentarios
    form_class = CrearComentarios

    def get_queryset(self):
        self.queryset =  self.model.objects.filter(id_publicacion = self.publicacion)
        return self.queryset

    def post(self, request, pk, *args, **kwargs):
        self.publicacion = get_object_or_404(Publicacion, id = pk)
        self.usuario = get_object_or_404(User, id = request.user.id)
        """ pk es el identificador de la publicacion"""
        query = self.get_queryset()
        form_ = self.form_class(request.POST)

        if form_.is_valid():
            comentario = form_.cleaned_data['comentario']
            """ Crear objeto del comentario """
            query.create(id_publicacion = self.publicacion, user = self.usuario, comentario = comentario)
        
        """ Listar los comentarios con ajax """
        if self.request.headers.get('x-requested-with'):
            """ se obtienen los comentarios de la publicacion y se pasan a la vista usando json """
            listado = []
            listadocomentarios = {}
            query.filter(id_publicacion = self.publicacion)

            objecto = query.last()
            listadocomentarios['url'] = objecto.user.get_absolute_url()
            listadocomentarios['id'] = objecto.id
            listadocomentarios['urlComentario'] = objecto.urlComentario()

            try: 
                objecto.user.foto
                listadocomentarios['img'] = objecto.user.foto.url
            except:
                listadocomentarios['img']="/static/img/default-profile.png" 

            listadocomentarios['apodo'] = objecto.user.apodo
            listadocomentarios['username'] = objecto.user.username
            listadocomentarios['comentario'] = objecto.comentario
            listadocomentarios['cantidad'] = query.count()
            listadocomentarios['pk'] =  self.publicacion.id
            listadocomentarios['urllikecomentario'] =  objecto.likeComentario()
            listado.append(listadocomentarios)

            listado = json.dumps(listado)
        return JsonResponse({'listadocomentarios': listado} )


""" Eliminar comentario de la publicacion """

class DeleteComentarioView(PreventGetMethodMixin, ValidateOwnershipMixin, LoginRequiredMixin, DeleteView):


    model = Comentarios

    def get_queryset(self):
        self.queryset =  self.model.objects.filter(id = self.kwargs["pk"])
        return self.queryset  

    def post(self, request, pk, *args, **kwargs):
        self.id_coment = pk
        query = self.get_queryset()
        cantidad = query.last()
        
        if query.filter(user = self.request.user).exists():
            query.delete()
            """ filtrar cantidad de comentarios en la publcacion """
        cantidad_likes = self.model.objects.filter(id_publicacion = cantidad.id_publicacion).count()
        result = {}
        listado = []
        result['cantidad'] = cantidad_likes
        result['pk'] = cantidad.id_publicacion.id
        listado.append(result)
        listado = json.dumps(listado)
        
        return JsonResponse({'json': listado} )

    def get_success_url(self) -> str:
        return reverse('detalle-publicacion', kwargs={'pk': self.get_object().id_publicacion.id, 'user_slug': self.get_object().user.slug})


""" Crear likes comentarios """

class AddLikesComentarios(PreventGetMethodMixin, LoginRequiredMixin, View):


    model = LikeComentarios

    def get_queryset(self, pk):
        self.queryset =  self.model.objects.filter(id = pk)
        return self.queryset


    def post(self, request, pk, *args, **kwargs):
        self.comentario = Comentarios.objects.get(id = pk)
        usuario = get_object_or_404(User, id = request.user.id)
        query = self.get_queryset(pk)
        cantidadlike = self.comentario.cantidadLikes()

        result = {}
        listado = []
        result['pk'] =  self.comentario.id
        result['url'] =  self.comentario.dislikeComentario()

        """ Si el usuario ya dio like devuelva la cantidad de likes que tiene la publicacion """

        if query.filter(user = self.request.user).exists(): 
            result['likes'] =  str(cantidadlike)
            listado.append(result)
            listado = json.dumps(listado)
            return JsonResponse({'result': listado} )
        """ Si no ha dado like se crea el objeto y se suma + 1  """
        query.create(id_comentario = self.comentario, user = usuario)

        cantidadlike += 1
        result['likes'] =  str(cantidadlike)
        listado.append(result)
        listado = json.dumps(listado)
        
        return JsonResponse({'result': listado} )

    def get_success_url(self) -> str:
        return reverse('detalle-publicacion', kwargs={'pk': self.publicacion.id, 'user_slug': self.publicacion.user.slug})



""" Eliminar likes en comentarios """

class RemoveLikesComentarios(ValidateOwnershipMixin, PreventGetMethodMixin, LoginRequiredMixin, View):

    model = LikeComentarios

    def get_queryset(self):
        self.queryset =  self.model.objects.get(id_comentario = self.kwargs["pk"], user = self.request.user)
        return self.queryset

    def get_object(self):
        return self.get_queryset()


    def post(self, request, pk, *args, **kwargs):
        """ la pk es el id de la publicacion para obtener el objeto """
        self.comentario = Comentarios.objects.get(id = pk)
        """ Se obtiene el usuario que da el no me gusta """
        self.get_queryset().delete()

        cantidadlike = self.comentario.cantidadLikes()

        result = {}
        listado = []
        result['pk'] =  self.comentario.id
        result['likes'] =  str(cantidadlike)

        result['url'] =  self.comentario.likeComentario()
        listado.append(result)
        listado = json.dumps(listado)
        return JsonResponse({'result': listado} )

    def get_success_url(self) -> str:
        return reverse('detalle-publicacion', kwargs={'pk': self.publicacion.id, 'user_slug': self.publicacion.user.slug})


""" Buscar elementos en la red social """

class BuscarContenidoView(ExtendsInnerContentMixin, LoginRequiredMixin, ListView):
    template_name = "social/user/buscar-contenido.html"
    model = Publicacion
    paginate_by = 5



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
            context_data['users'] = User.objects.filter((Q(username__icontains=query ) | Q(apodo__icontains=query)) &  Q(is_active=True)).order_by("-date_joined")[0:3]
        
            #TODO FILTRAR PRODUCTOS
            # context_data['productos'] 
        return context_data





    def get_queryset(self):
        
        # Si esta paginando que siga retornando los objetos
        if "page" in self.request.get_full_path():
            query = " "
            return Publicacion.objects.filter(Q(descripcion__icontains=query) | Q(user__apodo__icontains=query) | Q(user__username__icontains=query) 
                                                     | Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query) | 
                                                     Q(user__apodo__icontains=query)).order_by("-fecha_creacion")
        
        
        # En caso contrario revisa la query desde  0
        # Coge el query
        query = self.request.GET.get('q')

        if query:
            # Traducir el q url a formato entendible
            query = urllib.parse.unquote(query.lower())
            query = query.lower()
            special_characters = '"!@#$%^&*()-+?_=,<>/"'

            # Si la busqueda son solo espacios arrojaria error
            if len(query.replace(" ", "")) < 1:
                messages.add_message(self.request, 40, 'Busqueda vacia.')
                return []

            # Si tiene contenido
            else:
                # No permitir caracteres especiales
                if any(c in special_characters for c in query):
                    messages.add_message(self.request, 40, 'No se permiten caracteres especiales en la busqueda.')
                    return []
                else: 
                    # Retorna los objetos y quita los espacios al inicio y final de la busqueda
                    query = query.strip()
                    return Publicacion.objects.filter(Q(descripcion__icontains=query) | Q(user__apodo__icontains=query) | Q(user__username__icontains=query) 
                                                     | Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query) | 
                                                      Q(user__apodo__icontains=query)).order_by("-fecha_creacion")
        else:
            # Si no hay nada arroja error y no retorna ningun objeto
            
            return []


"""Busqueda Solo Usuarios"""

class BuscarUsuarioView(ExtendsInnerContentMixin, LoginRequiredMixin, ListView):
    model = User
    template_name = "social/user/buscar-user.html"
    paginate_by = 8
    ordering = "id"

    # get_Queryset Busqueda Usuario
    def get_queryset(self):

        # Si esta paginando que siga retornando los objetos
        if "page" in self.request.get_full_path():
            query = " "
            return User.objects.filter((Q(username__icontains=query ) | Q(apodo__icontains=query)) &  Q(is_active=True)).order_by("-date_joined")
        
        
        # En caso contrario revisa la query desde  0
        # Coge el query
        query = self.request.GET.get('q')

        if query:
            # Traducir el q url a formato entendible
            query = urllib.parse.unquote(query.lower())
            query = query.lower()
            special_characters = '"!@#$%^&*()-+?_=,<>/"'

            # Si la busqueda son solo espacios arrojaria error
            if len(query.replace(" ", "")) < 1:
                messages.add_message(self.request, 40, 'Busqueda vacia.')
                return []

            # Si tiene contenido
            else:
                # No permitir caracteres especiales
                if any(c in special_characters for c in query):
                    messages.add_message(self.request, 40, 'No se permiten caracteres especiales en la busqueda.')
                    return []
                else: 
                    # Retorna los objetos y quita los espacios al inicio y final de la busqueda
                    query = query.strip()
                    return User.objects.filter((Q(username__icontains=query ) | Q(apodo__icontains=query)) &  Q(is_active=True)).order_by("-date_joined")
        else:
            # Si no hay nada arroja error y no retorna ningun objeto
            messages.add_message(self.request, 40, 'Error en la busqueda.')
            return []
    
        



"""Vista de galeria"""


class GaleriaSocial(ExtendsInnerContentMixin, LoginRequiredMixin, ListView):
    model = Publicacion
    template_name = "social/user/galeria-social.html"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = get_object_or_404(User,slug = self.kwargs['slug'])
        return context

    def get_queryset(self):
        user = get_object_or_404(User,slug = self.kwargs['slug'])
        return Publicacion.objects.filter(Q(user=user) & ~Q(archivo="")).order_by("-fecha_creacion")

"""Vista de Seguir"""
#TODO PROBAR FUNCIONAMIENTO
class SeguirUsuario(PreventGetMethodMixin, LoginRequiredMixin, View):
    model = SeguidorUsuario

    def get_queryset(self):
        self.queryset = self.model.objects.filter(followed_user_id = self.usuario)
        return self.queryset

    def post(self, request, slug,  *args, **kwargs):
        self.usuario = get_object_or_404(User, slug=slug)

        if self.request.user == self.usuario:
            raise Http404()

        query = self.get_queryset()
        usuario_follower = get_object_or_404(User, id = request.user.id)

        cantidadFollows = len(self.usuario.get_user_followers())
        result = {}
        listado = []
        result['pk'] = self.usuario.id
        result['url'] = self.usuario.dejarseguirUsuario()

        """ Si el usuario ya dio like devuelva la cantidad de follows que tiene la publicacion """

        if query.filter(follower_user_id = self.request.user).exists(): 
            result['followers'] =  str(cantidadFollows)
            listado.append(result)
            listado = json.dumps(listado)
            return JsonResponse({'result': listado} )
        """ Si no ha dado like se crea el objeto y se suma + 1  """
        query.create(followed_user_id = self.usuario, follower_user_id =usuario_follower)
        cantidadFollows += 1
        result['followers'] =  str(cantidadFollows)
        listado.append(result)
        listado = json.dumps(listado)

        return JsonResponse({'result': listado} )


    def get_success_url(self) -> str:
        return reverse('detalle-creador', kwargs={'slug':self.usuario.slug})

"""Vista de Dejar Seguir"""
#TODO PROBAR FUNCIONAMIENTO
class DejarSeguirUsuario(PreventGetMethodMixin, LoginRequiredMixin, View):
    model = SeguidorUsuario

    def get_queryset(self):
        self.queryset = self.model.objects.filter(followed_user_id = self.usuario, follower_user_id = self.request.user)
        return self.queryset

    def get_object(self):
        return self.get_queryset()

    def post(self, request, slug,  *args, **kwargs):
    
        self.usuario = get_object_or_404(User, slug=slug)
        
        if self.request.user == self.usuario:
            raise Http404()

        query = self.get_queryset()
     
        query.delete()

        cantidadFollows = len(self.usuario.get_user_followers())
        result = {}
        listado = []
        result['pk'] = self.usuario.id
        result['url'] = self.usuario.seguirUsuario()
        result['followers'] =  str(cantidadFollows)

        listado.append(result)
        listado = json.dumps(listado)

        return JsonResponse({'result': listado} )


    def get_success_url(self) -> str:
        return reverse('detalle-creador', kwargs={'slug':self.usuario.slug})


"""Vista Lista Seguidores"""
    
class SeguidoresUsuario(ExtendsInnerContentMixin, LoginRequiredMixin, ListView):
    model = SeguidorUsuario
    paginate_by = 7
    template_name = 'social/user/seguidores.html'

    def get_queryset(self):
        # TODO ORDENAR LOS SEGUIDORES
        user = get_object_or_404(User, slug=self.kwargs['slug'])
        followers = user.get_user_followers()
       
        follower_list = []

        if self.request.user != user and self.request.user in followers:
            follower_list.append(self.request.user)
            followed = [followed.followed_user_id for followed in SeguidorUsuario.objects.filter(follower_user_id = self.request.user, followed_user_id__in=followers).order_by('followed_user_id__username')]
            for user in followed:
                follower_list.append(user)
            
            for user in followers:
                follower_list.append(user)


            follower_list = list(dict.fromkeys(follower_list))
            return follower_list

        return followers

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = get_object_or_404(User, slug=self.kwargs['slug'])
        return context


"""Vista Lista Seguidos"""
    
class SeguidosUsuario(ExtendsInnerContentMixin, LoginRequiredMixin, ListView):
    model = SeguidorUsuario
    paginate_by = 7
    template_name = 'social/user/seguidos.html'

    def get_queryset(self):
        user = get_object_or_404(User, slug=self.kwargs['slug'])
        followed = user.get_user_followed()

        # Ordenar los resultados:
        # Primero el request.user, luego los followed por el request.user
        # Finalmente los que no sigue

        if self.request.user != user:
            request_user_followed = self.request.user.get_user_followed()

            if request_user_followed:
                new_followed = []
                for user in request_user_followed:
                    if user in followed:
                        new_followed.append(user)
        
                followed = new_followed + followed
              

            if self.request.user in followed and followed[0] != self.request.user:
                followed = [self.request.user] + followed

            followed = list(dict.fromkeys(followed))
                

            
        # Si el usuario es el mismo al request.user se retorna directamente, puesto que ya
        # Vienen ordenados

        return followed

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = get_object_or_404(User, slug=self.kwargs['slug'])
        return context



