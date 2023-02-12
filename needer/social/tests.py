from django.test import TestCase
from .forms import CrearPublicacionForm
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Publicacion
from django.core.files import File

class TestPublicacionForm(TestCase):
    def test_crear_publicacion(self):
        """ Crear una publicacion de manera correcta """
        archivo = open('media/default-user.png', 'rb')
        form = CrearPublicacionForm(data={
                                          'descripcion':'Pruebas de testeo',
                                          'archivo':SimpleUploadedFile(archivo.name, archivo.read()),
                                          'NSFW':False})
        self.assertTrue(form.is_valid())


    def test_crear_publicacion_sin_archivo(self):
        """ Crear una publicacion sin archivo"""
        form = CrearPublicacionForm(data={
                                          'descripcion':'Pruebas de testeo',
                                          'NSFW':False})
        self.assertTrue(form.is_valid())

    """ Falta la 4 """

    def test_crear_publicacion_sin_datos(self):
        """ Crear una publicacion de manera correcta """
        form = CrearPublicacionForm(data={})
        self.assertFalse(form.is_valid())





        #self.assertEqual(
        #    form.errors['__all__'], ["Debes agregar una descripcion o un archivo a la publicacion."]
        #)
        
    
