from django.utils import timezone
from django import template
import mimetypes
from needer.settings import STATIC_URL
import os


register = template.Library()


def fecha_exacta(fecha):
    fecha_actual = timezone.now() - fecha

    if fecha_actual.days < 1:

        if fecha_actual.seconds < 60:
            return "Hace unos instantes"
        elif fecha_actual.seconds < 3600 and fecha_actual.seconds > 60:
            return "{} min".format(round(fecha_actual.seconds/60))
        else:
            return "{} h".format(round(fecha_actual.seconds/3600))

    elif fecha_actual.days > 1 and fecha_actual.days < 2:
        return "Ayer a las {}".format(fecha.strftime('%H:%M').lower())

    else:
        return "{} de {} a las {}".format(fecha.strftime('%d'), fecha.strftime('%B'), fecha.strftime('%H:%M'))


def editado(publicacion):

    if publicacion.fecha_actualizacion > publicacion.fecha_creacion :
        return '<small class="text-muted editado">Editado <i class="bi bi-pencil text-primary"></i></small>'
    else:
        return None


def tipo_archivo(archivo):
    
    # retorna el tipo de archivo
    content = mimetypes.guess_type(archivo.url, strict=True)[0]

    if content.split('/')[0] == 'image':
        return f'<img class="img-fluid pub-img rounded" src="{archivo.url}" alt="profile" data-holder-rendered="true"/>'

    elif content.split('/')[0] == 'audio':
        return f'<audio controls controlsList="nodownload"> <source src="{archivo.url}" type="audio/mpeg">Your browser does not support the audio tag.</audio>'

    elif content.split('/')[0] == 'video':
        return f'<video class="pub-video img-fluid rounded" controls controlsList="nodownload"> <source src="{archivo.url}">Your browser does not support the video tag.</video>'


def nsfw(value):

    if value:
        return 'nsfw'

    return ''

# TODO AGREGAR LA PARTE DEL MARKETPLACE
@register.simple_tag
def busquedaVacia(users, object_list):

    if not users and len(object_list) == 0:
        return f'''<div class="row container my-auto mt-2 d-flex justify-content-center">
       
        <img
        class="mt-4 mb-3 img-fluid img-busqueda"
        src="/{os.path.join(STATIC_URL,'img/void.svg')}"
        >
        <h3 class="text-center ">No se encontro nada referente a tu busqueda</h3>
        <h6 class="text-center ">Prueba con otras palabras claves o quita los filtros de busqueda</h6>
    </div>'''
    elif len(users) == 0 and len(object_list) == 0:
        return f'''<div class="row container mt-2 my-auto d-flex justify-content-center">
       
        <img
        class="mt-4 mb-3 img-fluid img-busqueda"
        src="/{os.path.join(STATIC_URL,'img/void.svg')}"
        >
        <h3 class="text-center ">No se encontro nada referente a tu busqueda</h3>
        <h6 class="text-center ">Prueba con otras palabras claves o quita los filtros de busqueda</h6>
    </div>'''
    
    else:
        return False


    

register.filter('nsfw', nsfw)
register.filter('tipo_archivo', tipo_archivo)
register.filter('editado', editado)
register.filter('fecha_exacta', fecha_exacta)
register.filter("busqueda_vacia", busquedaVacia)