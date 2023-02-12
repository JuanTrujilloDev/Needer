from django.test import TestCase
from .forms import SignupCustomForm
from .models import Pais, User
from http import HTTPStatus

class TestUserForm(TestCase):

    def test_registro_plataforma(self): 
        """ R-1 Registro en la plataforma de forma correcta """
        Pais.objects.create(nombre='Colombia')
        form = SignupCustomForm(data={
            'username':'Juan',
            'email':'puentesjs903@gmail.com',
            'first_name':'Juan',
            'last_name': 'Puentes',
            'password1': 'sebas_111@',
            'password2': 'sebas_111@',
            'pais':      'Colombia',
            'num_documento':'1075316291'
        })    
        self.assertTrue(form.is_valid())

    def test_registro_plataforma_error_documento(self):
        """ R-2 Registro en la plataforma con error en el documento vacio"""
        Pais.objects.create(nombre='Colombia')
        form = SignupCustomForm(data={
            'username':'Juan',
            'email':'puentesjs903@gmail.com',
            'first_name':'Juan',
            'last_name': 'Puentes',
            'password1': 'sebas_111@',
            'password2': 'sebas_111@',
            'pais':      'Colombia',
            'num_documento': 'aaaaa9810'
        })    

        self.assertEqual(
            form.errors['num_documento'],['Error en el numero de documento debe contener solo numeros (De 6 - 10 numeros).']
            )
        
    def test_registro_plataforma_error_email(self):
        """ R-3 Error con el email sintaxis no valida """
        Pais.objects.create(nombre='Colombia')
        form = SignupCustomForm(data={
            'username':'Juan',
            'email':'puentesjs903@gmail',
            'first_name':'Juan',
            'last_name': 'Puentes',
            'password1': 'sebas_111@',
            'password2': 'sebas_111@',
            'pais':      'Colombia',
            'num_documento': '1075316291'
        })  
        self.assertEqual(
            form.errors['email'],['Introduzca una dirección de correo electrónico válida.']
            )
        
    def test_registro_plataforma_error_password(self):
        """ R-4 Error con la contraseña """
        Pais.objects.create(nombre='Colombia')
        form = SignupCustomForm(data={
            'username':'Juan',
            'email':'puentesjs903@gmail.com',
            'first_name':'Juan',
            'last_name': 'Puentes',
            'password1': '123',
            'password2': '123',
            'pais':      'Colombia',
            'num_documento': '1075316291'
        })  
        self.assertFalse(
            form.is_valid()
        )

    def test_registro_plataforma_error_username(self):
        """ R-5 Error con el usuario """
        Pais.objects.create(nombre='Colombia')
        form = SignupCustomForm(data={
            'username':'',
            'email':'puentesjs903@gmail.com',
            'first_name':'Juan',
            'last_name': 'Puentes',
            'password1': 'sebas_@1998',
            'password2': 'sebas_@1998',
            'pais':      'Colombia',
            'num_documento': '1075316291'
        }) 
        self.assertEqual(
            form.errors['username'], ['Este campo es obligatorio.']
        )

    def test_registro_plataforma_error_first_name(self):
        """ R-6 Error con el first_name """
        Pais.objects.create(nombre='Colombia')
        form = SignupCustomForm(data={
            'username':'juan',
            'email':'puentesjs903@gmail.com',
            'first_name':'',
            'last_name': 'Puentes',
            'password1': 'sebas_@1998',
            'password2': 'sebas_@1998',
            'pais':      'Colombia',
            'num_documento': '1075316291'
        }) 
        self.assertEqual(
            form.errors['first_name'], ['Este campo es obligatorio']
        )

    def test_registro_plataforma_error_last_name(self):
        """ R-7 Error con el last_name """
        Pais.objects.create(nombre='Colombia')
        form = SignupCustomForm(data={
            'username':'juan',
            'email':'puentesjs903@gmail.com',
            'first_name':'Juan',
            'last_name': '',
            'password1': 'sebas_@1998',
            'password2': 'sebas_@1998',
            'pais':      'Colombia',
            'num_documento': '1075316291'
        }) 
        self.assertEqual(
            form.errors['last_name'], ['Este campo es obligatorio']
        )

    def test_registro_plataforma_error_pais(self):
        """ R-8 Error con el pais """
        Pais.objects.create(nombre='Colombia')
        form = SignupCustomForm(data={
            'username':'juan',
            'email':'puentesjs903@gmail.com',
            'first_name':'Juan',
            'last_name': 'Puentes',
            'password1': 'sebas_@1998',
            'password2': 'sebas_@1998',
            'pais':      'Brazil',
            'num_documento': '1075316291'
        }) 
        self.assertEqual(
            form.errors['pais'], ['El pais no se encuentra en la lista']
        )

    def test_registro_plataforma_datos_duplicados(self):
        """ R-9 Datos duplicados """
        pais = Pais.objects.create(nombre='Colombia')
        User.objects.create(
            username='juan',
            email='puentesjs903@gmail.com',
            first_name='Juan',
            last_name= 'Puentes',
            password= 'sebas_@1998',
            pais =      pais,
            num_documento= '1075316291'
        ) 
        form = SignupCustomForm(data={
            'username':'juan',
            'email':'puentesjs903@gmail.com',
            'first_name':'Juan',
            'last_name': 'Puentes',
            'password1': 'sebas_@1998',
            'password2': 'sebas_@1998',
            'pais':      'Colombia',
            'num_documento': '1075316291'
        }) 
        self.assertFalse(form.is_valid())

    def test_registro_plataforma_sin_datos(self):
        """ R-10 Se envia un formulario vacio """

        form = SignupCustomForm(data={
            'username':'',
            'email':'',
            'first_name':'',
            'last_name': '',
            'password1': '',
            'password2': '',
            'pais':      '',
            'num_documento': ''
        }) 
        self.assertFalse(
            form.is_valid()
        )

