from django.test import TestCase
from .forms import ThreadForm
from users.models import User, Pais
from .models import Thread, ChatMessage
from allauth.account.models import EmailAddress

class TestChat(TestCase):
    def setUp(self) -> None:
        """ Creacion de objetos """
        self.pais = Pais.objects.create(nombre='Colombia')

        """ Usuarios de los hilos """
        self.first_person = User.objects.create_user(email='gamesappeveryone@gmail.com', password='sebas_1998', username='chika', pais=self.pais)
        self.second_person = User.objects.create_user(email='puentesjs903@gmail.com', password='sebas_1998', username='juan', pais=self.pais)
        
        """ Este usuario no va a pertenecer a ningun hilo """
        self.three_person = User.objects.create_user(email='carlosjs@gmail.com', password='sebas_1998', username='carlos', pais=self.pais)

        """ Verificacion de correo de los dos usuarios del hilo"""
        EmailAddress.objects.create(user=self.first_person, email='gamesappeveryone@gmail.com', verified=True, primary=True)
        EmailAddress.objects.create(user=self.second_person, email='puentesjs903@gmail.com', verified=True, primary=True)
        EmailAddress.objects.create(user=self.second_person, email='carlosjs@gmail.com', verified=True, primary=True)

        """ Hilo creado """
        self.thread = Thread.objects.create(first_person=self.first_person, second_person=self.second_person)
        return super().setUp()
    

    def test_crear_hilo(self):
        """ Contar si se creo el hilo del setup """
        object_count = Thread.objects.all().count()
        self.assertNotEqual(object_count, 0)


    def test_crear_hilo_error(self):
        """ No se crea un hilo porque ya existe """
        try:
            Thread.objects.create(first_person=self.first_person, second_person=self.second_person)
            thread2 = False
        except:
            thread2=True
        
        self.assertTrue(thread2)


    def test_crear_mensaje(self):
        message = 'Mensaje de prueba'
        """ Se crea un nuevo mensaje en el hilo """
        ChatMessage.objects.create(thread = self.thread, user=self.first_person, message=message)
        countmessage = ChatMessage.objects.all().count()
        """ Debe haber 1 mensaje, el que se acaba de crear"""
        self.assertEqual(countmessage,1)


    def test_error_mensaje_usuario_no_pertenece_al_hilo(self):
        message = 'Mensaje de prueba'
        """ Se crea un nuevo mensaje en el hilo """
        try:
            ChatMessage.objects.create(thread = self.thread, user=self.three_person, message=message)
            countmessage = 1
        except:
            countmessage = ChatMessage.objects.all().count()
        """ Debe haber 1 mensaje, el que se acaba de crear en el test anterior"""
        self.assertEqual(countmessage,0)

    
    def test_error_mensaje_vacio(self):
        """ Se envia el parametro message vacio """
        try:
            ChatMessage.objects.create(thread = self.thread, user=self.first_person, message='')
            message = ['Mensaje creado correctamente']
        except:
            message = ['Mensaje vacio']
        self.assertEqual(message, ['Mensaje vacio'])


        
