from django.urls import path
from .views import *



urlpatterns = [

    # Lista red social
    path('home/', HomeSocialView.as_view(), name='social-home'),

    # CREADOR DE CONTENIDO DETAIL
    
    path('<str:slug>/', DetailCreador.as_view(), name='detalle-creador'),




    # CRUD PUBLICACION:
    path('<str:user_slug>/publicacion/<int:pk>', DetallePublicacionView.as_view(), name='detalle-publicacion'),
    path('publicacion/create', CrearPublicacionView.as_view(), name='crear-publicacion'),
    path('<str:user_slug>/publicacion/<int:pk>/update', UpdatePublicacionView.as_view(), name='update-publicacion'),
    path('<str:user_slug>/publicacion/<int:pk>/delete', DeletePublicacionView.as_view(), name='delete-publicacion'),
    

    #likes
    path('publicacion/<int:pk>/like', AddLikesPublicacion.as_view(), name= 'addlike'),
    path('publicacion/<int:pk>/dislike', RemoveLikesPublicacion.as_view(), name= 'removelike'),


    #Comentarios
    path('comentario/<int:pk>', CrearComentarioView.as_view(), name= 'comentario'),
    path('comentario/<int:pk>/delete/<str:user_slug>', DeleteComentarioView.as_view(), name= 'delete-comentario'),
    path('comentario/<int:pk>/like', AddLikesComentarios.as_view(), name= 'comentario-addlike'),
    path('comentario/<int:pk>/dislike', RemoveLikesComentarios.as_view(), name= 'comentario-removelike'),
]