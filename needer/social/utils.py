from datetime import datetime
import uuid
from django.core.exceptions import ValidationError
import os
from django.conf import settings
from PIL import Image
from io import BytesIO
import sys
from PIL import Image

def postDirectory(instance, filename):
    '''
    
    #TODO Documentar
    
    '''
    fecha = datetime.now()
    # Se guarda en account/usuario/publicacion/anio/mes/dia
    profile_picture_name = 'account/{0}/publicacion/{2.year}/{2.month}/{2.day}/{1}'.format(instance.user.username, filename, fecha)
    return profile_picture_name


# Funcion para validar que la extension sea correcta
def valid_file_extention(value):
    '''
    
    #TODO Documentar
    
    '''


    # Se valida que las extensiones sean correctas.
    ext = os.path.splitext(value.name)[1]
    valid_extentions = ['.jpg', '.png', '.gif', '.jpeg', '.mp3', '.mp4', '.wav', '.m4a', '.mov', '.avi', '.mkv', '.webm']


    # Se valida el tipo de contenido
    valid_content = ['image', 'video', 'audio']
    content_type = value.file.content_type.split('/')[0]
    if content_type not in valid_content:
        raise ValidationError('Solo se permiten Imagenes, Videos o Audios.')
    

    # Si el archivo no se encuentra en las extensiones permitidas
    if not ext.lower() in valid_extentions:
        raise ValidationError('El formato del archivo no es soportado, por favor utiliza cualquiera de los formatos permitidos. \n{0}'.format(valid_extentions))




# Funcion para validar tamano del archivo:

def valid_file_size(value):

    # 50MB - 5242880 Si el archivo es mayor a 50 Mb arrojara error.
    if value.file.size > 52428800:
        raise ValidationError(f"El archivo debe ser menor a 50Mb, este pesa: {round((value.file.size/1024/1000), 2)}Mb")


    
    




def file_compression(value):
    '''
    
    #TODO Documentar
    
    '''
    content = value.file.content_type.split('/')[0]

    # Si el archivo es imagen
    if content == 'image':
        # Opening uploaded image

        ext = os.path.splitext(value.name)[1]
        # Si es un gif que lo guarde de una vez
        if ext == '.gif':
            return value


        im = Image.open(value)

        output = BytesIO()

        # Comprimiendo la imagen
        im.save(output, quality=80)
        output.seek(9)



        return im

    # Si el archivo es video no hace nada debido a que no
    # se puede comprimir
    elif content == 'video':
        value.name = value.name.split('.')[0] + str(uuid.uuid1()) + '.mp4'
        return value

    

    # Si el archivo es audio:
    elif content == 'audio':

        value.name = value.name.split('.')[0] + str(uuid.uuid1()) + '.mp3'
        return value

        





        






    