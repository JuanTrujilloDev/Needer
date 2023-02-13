from django.test import TestCase
from .forms import CrearPublicacionForm, CrearComentarios
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Publicacion, Comentarios
from django.core.files import File

class TestPublicacionForm(TestCase):
    def test_crear_publicacion(self):
        """ Crear una publicacion de manera correcta """
        archivo = open('media/default-user.png', 'rb')
        file = SimpleUploadedFile('default-user.png', content=archivo.read(), content_type='image/jpeg')
        form = CrearPublicacionForm({'descripcion':'Descripcion', 'nsfw':True}, {'archivo':file})

        self.assertTrue(form.is_valid())


    def test_crear_publicacion_sin_archivo(self):
        """ Crear una publicacion sin archivo"""
        form = CrearPublicacionForm(data={
                                          'descripcion':'Pruebas de testeo',
                                          'NSFW':False})
        self.assertTrue(form.is_valid())

    def test_crear_publicacion_sin_descripcion(self):
        archivo = open('media/default-user.png', 'rb')
        file = SimpleUploadedFile('default-user.png', content=archivo.read(), content_type='image/jpeg')
        form = CrearPublicacionForm({'descripcion':'', 'nsfw':True},{'archivo':file,})
        self.assertTrue(form.is_valid())

    def test_crear_publicacion_sin_datos(self):
        """ Crear una publicacion de manera correcta """
        form = CrearPublicacionForm(data={})
        self.assertFalse(form.is_valid())




class TestComentarioForm(TestCase):
    def test_comentar_publicacion(self):
        """ C-1 crear comentario"""
        form = CrearComentarios(data={'comentario':'Pruebas de testeo'})
        self.assertTrue(form.is_valid())
        
    def test_comentar_publicacion_vacia(self):
        """ C-2 comentario vacio """
        form = CrearComentarios(data={'comentario':''})
        self.assertFalse(form.is_valid())
        
    
