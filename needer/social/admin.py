from django.contrib import admin

from .models import Publicacion, LikedPublicacion, Comentarios, LikeComentarios

# Register your models here.


#Registro de modelos
admin.site.register(Publicacion)
admin.site.register(LikedPublicacion)
admin.site.register(Comentarios)
admin.site.register(LikeComentarios)

