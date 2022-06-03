from django.urls import path
from .views import *



urlpatterns = [

    # CREADOR DE CONTENIDO DETAIL
    
    path('<str:slug>/', DetailCreador.as_view(), name='detalle-creador'),




    path('<str:user_slug>/publicacion/<int:pk>', DetallePublicacionView.as_view(), name='detalle-publicacion'),


    # VISTAS PARA SOLO EL CREADOR DE CONTENIDO:

    path('publicacion/create', CrearPublicacionView.as_view(), name='crear-publicacion'),
    # path('<str:user_slug>/publicacion/<int:pk>/update', UpdatePublicacion.as_view(), name='update-publicacion'),
    # path('<str:user_slug>/publicacion/<int:pk>/delete', DeletePublicacion.as_view(), name='update-publicacion'),
    


]