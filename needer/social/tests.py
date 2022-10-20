from django.test import TestCase

from users.models import User
from .models import Comentarios, Publicacion 
# Create your tests here.

class TestPublicacion(TestCase):
    fixtures = ['db']

    def creador_publicacion(self):
        Publicacion.objects.create(
            user = User.objects.get(id =2),
            descripcion = "Publicacion de pruebas",
            archivo = "",
            nsfw = False
        )
        self.ulti_publicacion = Publicacion.objects.last()
        return self.ulti_publicacion
        

    def test_creacion_publicaciones(self):
        """ Se obtiene la cantidad de publicaciones para 
            verificar si se creo una nueva publicacion """
        n_publi = Publicacion.objects.all().count()
        self.creador_publicacion()
        """ Como se creo una publicacion debe haber una publicacion mas """
        n_new_publi = Publicacion.objects.all().count()
        self.assertNotEqual(n_publi, n_new_publi)
        

    def test_eliminar_publicacion(self):
        publi = Publicacion.objects.first()
        pk = publi.pk
        publi.delete()
        """ Obtiene el objeto """
        a = Publicacion.objects.filter(pk = pk)
        """ Verifica si se borro el objeto """
        self.assertEqual(a.count(), 0)


class TestComentario(TestCase):
    fixtures = ['db']

    def creador_comentario(self):
        Comentarios.objects.create(
            id_publicacion = Publicacion.objects.get(pk = 117),
            id_autor = User.objects.get(id =2),
            comentario = 'Hola bb que mas pues :3',

    
        )
        self.ulti_comentario = Comentarios.objects.last()
        return self.ulti_comentario

    def test_creacion_comentario(self):
        n_publi = Comentarios.objects.filter(id_publicacion = 117).count()
        self.creador_comentario()
        n_new_publi = Comentarios.objects.filter(id_publicacion = 117).count()
        self.assertNotEqual(n_publi, n_new_publi)


    def test_eliminar_publicacion(self):
        self.creador_comentario()
        coment = Comentarios.objects.last()
        pk = coment.pk
        coment.delete()
        """ Obtiene el objeto """
        a = Comentarios.objects.filter(pk = pk)
        """ Verifica si se borro el objeto """
        self.assertEqual(a.count(), 0)
    
