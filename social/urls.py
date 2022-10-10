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
    # path('<str:user_slug>/publicacion/<int:pk>/delete', DeletePublicacion.as_view(), name='update-publicacion'),
    

    #likes
    

]