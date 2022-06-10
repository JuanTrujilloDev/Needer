from django.utils import timezone
from django import template
import mimetypes

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
        return '<small class="text-muted">Editado <i class="bi bi-pencil text-primary"></i></small>'
    else:
        return None


def tipo_archivo(archivo):
    
    # retorna el tipo de archivo
    content = mimetypes.guess_type(archivo.url, strict=True)[0]
    print(content)
    if content.split('/')[0] == 'image':
        return f'<img class="img-fluid pub-img rounded" src="{archivo.url}" alt="profile" data-holder-rendered="true"/>'

    elif content.split('/')[0] == 'audio':
        return f'<audio controls controlsList="nodownload"> <source src="{archivo.url}" type="audio/mpeg">Your browser does not support the audio tag.</audio>'

    elif content.split('/')[0] == 'video':
        return f'<video class="pub-video" controls controlsList="nodownload"> <source src="{archivo.url}">Your browser does not support the video tag.</video>'


register.filter('tipo_archivo', tipo_archivo)
register.filter('editado', editado)
register.filter('fecha_exacta', fecha_exacta)