from django.test import TestCase, Client
from .forms import SignupCustomForm, UpdateUserForm
from .models import Pais, User, TipoCelebridad
from django.urls import reverse
from django.conf import settings
from allauth.account.models import EmailAddress
from unittest.mock import patch
from captcha.client import RecaptchaResponse
import datetime
from django.core.files.uploadedfile import SimpleUploadedFile

class TestUserForm(TestCase):
    @patch("captcha.fields.client.submit")
    def test_registro_plataforma(self, mocked_submit): 
        """ R-1 Registro en la plataforma de forma correcta """
        Pais.objects.create(nombre='Colombia')
        mocked_submit.return_value = RecaptchaResponse(is_valid=True)
        form = SignupCustomForm(data={
            'username':'Juan',
            'email':'puentesjs903@gmail.com',
            'first_name':'Juan',
            'last_name': 'Puentes',
            'password1': 'sebas_111@',
            'password2': 'sebas_111@',
            'pais':      'Colombia',
            'num_documento':'1075316291',
            'captcha': 'PASSED'
        })    
        self.assertTrue(form.is_valid())


    @patch("captcha.fields.client.submit")
    def test_registro_plataforma_error_documento(self, mocked_submit):
        """ R-2 Registro en la plataforma con error en el documento vacio"""
        Pais.objects.create(nombre='Colombia')
        mocked_submit.return_value = RecaptchaResponse(is_valid=True)
        form = SignupCustomForm(data={
            'username':'Juan',
            'email':'puentesjs903@gmail.com',
            'first_name':'Juan',
            'last_name': 'Puentes',
            'password1': 'sebas_111@',
            'password2': 'sebas_111@',
            'pais':      'Colombia',
            'num_documento': 'aaaaa9810',
            'captcha': 'PASSED'
        })    

        self.assertEqual(
            form.errors['num_documento'],['Error en el numero de documento debe contener solo numeros (De 6 - 10 numeros).']
            )

    @patch("captcha.fields.client.submit")    
    def test_registro_plataforma_error_email(self, mocked_submit):
        """ R-3 Error con el email sintaxis no valida """
        Pais.objects.create(nombre='Colombia')
        mocked_submit.return_value = RecaptchaResponse(is_valid=True)
        form = SignupCustomForm(data={
            'username':'Juan',
            'email':'puentesjs903@gmail',
            'first_name':'Juan',
            'last_name': 'Puentes',
            'password1': 'sebas_111@',
            'password2': 'sebas_111@',
            'pais':      'Colombia',
            'num_documento': '1075316291',
            'captcha': 'PASSED'
        })  
        self.assertEqual(
            form.errors['email'],['Introduzca una dirección de correo electrónico válida.']
            )

    @patch("captcha.fields.client.submit")    
    def test_registro_plataforma_error_password(self, mocked_submit):
        """ R-4 Error con la contraseña """
        Pais.objects.create(nombre='Colombia')
        mocked_submit.return_value = RecaptchaResponse(is_valid=True)
        form = SignupCustomForm(data={
            'username':'Juan',
            'email':'puentesjs903@gmail.com',
            'first_name':'Juan',
            'last_name': 'Puentes',
            'password1': '123',
            'password2': '123',
            'pais':      'Colombia',
            'num_documento': '1075316291',
            'captcha': 'PASSED'
        })  
        self.assertFalse(
            form.is_valid()
        )

    @patch("captcha.fields.client.submit")   
    def test_registro_plataforma_error_username(self, mocked_submit):
        """ R-5 Error con el usuario """
        Pais.objects.create(nombre='Colombia')
        mocked_submit.return_value = RecaptchaResponse(is_valid=True)
        form = SignupCustomForm(data={
            'username':'',
            'email':'puentesjs903@gmail.com',
            'first_name':'Juan',
            'last_name': 'Puentes',
            'password1': 'sebas_@1998',
            'password2': 'sebas_@1998',
            'pais':      'Colombia',
            'num_documento': '1075316291',
            'captcha': 'PASSED'
        }) 
        self.assertEqual(
            form.errors['username'], ['Este campo es obligatorio.']
        )

    @patch("captcha.fields.client.submit")   
    def test_registro_plataforma_error_first_name(self, mocked_submit):
        """ R-6 Error con el first_name """
        Pais.objects.create(nombre='Colombia')
        mocked_submit.return_value = RecaptchaResponse(is_valid=True)
        form = SignupCustomForm(data={
            'username':'juan',
            'email':'puentesjs903@gmail.com',
            'first_name':'',
            'last_name': 'Puentes',
            'password1': 'sebas_@1998',
            'password2': 'sebas_@1998',
            'pais':      'Colombia',
            'num_documento': '1075316291',
            'captcha': 'PASSED'
        }) 
        self.assertEqual(
            form.errors['first_name'], ['Este campo es obligatorio']
        )

    @patch("captcha.fields.client.submit")   
    def test_registro_plataforma_error_last_name(self, mocked_submit):
        """ R-7 Error con el last_name """
        Pais.objects.create(nombre='Colombia')
        mocked_submit.return_value = RecaptchaResponse(is_valid=True)
        form = SignupCustomForm(data={
            'username':'juan',
            'email':'puentesjs903@gmail.com',
            'first_name':'Juan',
            'last_name': '',
            'password1': 'sebas_@1998',
            'password2': 'sebas_@1998',
            'pais':      'Colombia',
            'num_documento': '1075316291',
            'captcha': 'PASSED'
        }) 
        self.assertEqual(
            form.errors['last_name'], ['Este campo es obligatorio']
        )

    @patch("captcha.fields.client.submit")   
    def test_registro_plataforma_error_pais(self, mocked_submit):
        """ R-8 Error con el pais """
        Pais.objects.create(nombre='Colombia')
        mocked_submit.return_value = RecaptchaResponse(is_valid=True)
        form = SignupCustomForm(data={
            'username':'juan',
            'email':'puentesjs903@gmail.com',
            'first_name':'Juan',
            'last_name': 'Puentes',
            'password1': 'sebas_@1998',
            'password2': 'sebas_@1998',
            'pais':      'Brazil',
            'num_documento': '1075316291',
            'captcha': 'PASSED'
        }) 
        self.assertEqual(
            form.errors['pais'], ['El pais no se encuentra en la lista']
        )

    @patch("captcha.fields.client.submit")   
    def test_registro_plataforma_datos_duplicados(self, mocked_submit):
        """ R-9 Datos duplicados """
        pais = Pais.objects.create(nombre='Colombia')
        mocked_submit.return_value = RecaptchaResponse(is_valid=True)
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
            'num_documento': '1075316291',
            'captcha': 'PASSED'
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



class TestUserLogin(TestCase):
    def setUp(self):
        self.credenciales = {
            'login':'puentesjs903@gmail.com',
            'password':'sebas_1998',
        }
        self.client = Client()
        self.user = User.objects.create_user(email='puentesjs903@gmail.com', password='sebas_1998', username='juan')
        self.email = EmailAddress.objects.create(user=self.user, email='puentesjs903@gmail.com', verified=True, primary=True)
        return super().setUp()

    def test_autenticacion_usuario(self):
        """  A- 1 Ingreso a la plataforma """
        response = self.client.post(reverse('account_login'),self.credenciales)
        self.assertRedirects(response, settings.LOGIN_REDIRECT_URL, fetch_redirect_response=False) 

    def test_autenticacion_usuario_sin_cuenta_activa(self):
        """ A- 2  Autenticacion del usuario sin tener una cuenta activa """
        response = self.client.post(reverse('account_login'),{"login":"no_estoy_registrado@gmail.com","password":"wrong"})
        validador_error = 'El correo electrónico y/o la contraseña que se especificaron no son correctos.'
        assert validador_error in response.content.decode('utf-8')

    def test_autenticacion_usuario_error_password(self):
        """ A-3 Error en la contraseña del usuario """
        response = self.client.post(reverse('account_login'),{'login':'puentesjs903@gmail.com', 'password':'a'})
        validador_error = 'El correo electrónico y/o la contraseña que se especificaron no son correctos.'
        assert validador_error in response.content.decode('utf-8')
    
    def test_autenticacion_usuario_error_email(self):
        """ A-4  Error en el email del usuario"""
        response = self.client.post(reverse('account_login'),{'login':'puentesjs@gmail', 'password':'sebas_1998'})
        validador_error = 'Introduzca una dirección de correo electrónico válida.'
        assert validador_error in response.content.decode('utf-8')

    def test_autenticacion_usuario_datos_vacios(self):
        """ A-5 Intento de autenticacion con datos vacios"""
        response = self.client.post(reverse('account_login'),{'login':'', 'password':''})
        validador_error = 'Este campo es obligatorio.'  
        assert validador_error in response.content.decode('utf-8')


class TestActualizacionPerfilForm(TestCase):
    def autenticacion(self):
        self.credenciales = {
            'login':'puentesjs903@gmail.com',
            'password':'sebas_1998',
        }
        self.client = Client()
        self.pais = Pais.objects.create(nombre='Colombia')
        User.objects.create_user(email='puentesjs@gmail.com', password='sebas_1998', username='pedro', pais=self.pais)
        self.user = User.objects.create_user(email='puentesjs903@gmail.com', password='sebas_1998', username='juan', pais=self.pais)
        self.email = EmailAddress.objects.create(user=self.user, email='puentesjs903@gmail.com', verified=True, primary=True)
        """  Login """
        self.client.post(reverse('account_login'),self.credenciales)


    def setUp(self) -> None:
        """ Login """
        self.autenticacion()
        """ Archivos """
        foto_ = open('media/default-user.png', 'rb')
        banner_ = open('media/default-user.png', 'rb')
        foto = SimpleUploadedFile('default-user.png', content=foto_.read(), content_type='image/jpeg')
        banner =  SimpleUploadedFile('default-user.png', content=banner_.read(), content_type='image/jpeg')

        """ Creacion de objetos Pais y Tipo_Celebridad para actualizar los datos """
        """ tipo_celebridad = TipoCelebridad.objects.create('Actor') """
        
        self.first_name = 'Juan Sebastian' 
        self.last_name = 'Puentes Coronado'
        self.pais = self.pais
        self.username = 'Barvabavaba' 
        self.apodo='Barrava' 
        self.fecha_nacimiento = datetime.datetime(1998, 10, 13)
        self.genero = 'Hombre'
        """ self.tipo_celebridad = tipo_celebridad """
        self.foto = foto
        self.biografia ='Descripcion de la biografia'
        self.link = "www.needer.co"
        self.banner = banner
        return super().setUp()
    
    def test_actualizacion_datos(self):
        """ AP-1 Actualizacion del perfil """
        form = UpdateUserForm({'first_name':self.first_name, 
                               'last_name':self.last_name,
                               'pais': self.pais,
                               'username':self.username,
                               'apodo':self.apodo,
                               'link':self.link,
                               'biografia':self.biografia,
                               'genero':self.genero,
                               'fecha_nacimiento':self.fecha_nacimiento}, {'foto':self.foto, 'banner':self.banner}, instance = self.user)

        self.assertTrue(form.is_valid())

    def test_actualizacion_datos_error_username(self):
        """ AP-2 Actualizacion perfil error en el username """
        """ Pedro ya esta registrado en el en la db y no puede haber otro usuario
        con el mismo username """
        form = UpdateUserForm({'first_name':self.first_name, 
                               'last_name':self.last_name,
                               'pais': self.pais,
                               'username':'Pedro',
                               'apodo':self.apodo,
                               'link':self.link,
                               'biografia':self.biografia,
                               'genero':self.genero,
                               'fecha_nacimiento':self.fecha_nacimiento}, {'foto':self.foto, 'banner':self.banner}, instance = self.user)
        self.assertEqual(form.errors['username'],['El nombre de usuario ya se encuentra registrado, intenta con otro.'])
    
    def test_actualizacion_datos_error_first_name(self):
        """ AP-3 Actualizacion perfil error en el first_name """
        form = UpdateUserForm({'first_name':'carlos', 
                               'last_name':self.last_name,
                               'pais': self.pais,
                               'username':self.username,
                               'apodo':self.apodo,
                               'link':self.link,
                               'biografia':self.biografia,
                               'genero':self.genero,
                               'fecha_nacimiento':self.fecha_nacimiento}, {'foto':self.foto, 'banner':self.banner}, instance = self.user)
        self.assertEqual(form.errors['first_name'],['Formato Invalido. El nombre debe contener solo letras y empezar por mayuscula.'])


    def test_actualizacion_datos_error_last_name(self):
        """ AP-4 Actualizacion perfil error en el last_name """
        form = UpdateUserForm({'first_name':self.first_name, 
                               'last_name':'puentes',
                               'pais': self.pais,
                               'username':self.username,
                               'apodo':self.apodo,
                               'link':self.link,
                               'biografia':self.biografia,
                               'genero':self.genero,
                               'fecha_nacimiento':self.fecha_nacimiento}, {'foto':self.foto, 'banner':self.banner}, instance = self.user)
        self.assertEqual(form.errors['last_name'],['Formato Invalido. El nombre debe contener solo letras y empezar por mayuscula.'])


    def test_actualizacion_datos_error_pais(self):
        """ AP-5 Actualizacion perfil error en el pais """
        form = UpdateUserForm({'first_name':self.first_name, 
                               'last_name':self.last_name,
                               'pais': 'China Cominista uwu',
                               'username':self.username,
                               'apodo':self.apodo,
                               'link':self.link,
                               'biografia':self.biografia,
                               'genero':self.genero,
                               'fecha_nacimiento':self.fecha_nacimiento}, {'foto':self.foto, 'banner':self.banner}, instance = self.user)
        self.assertEqual(form.errors['pais'],['El pais no se encuentra en la lista'])

    def test_actualizacion_datos_campos_vacios(self):
        """ AP-5 Actualizacion perfil error en los campos vacios """
        form = UpdateUserForm({'first_name':'', 
                               'last_name':'',
                               'pais': '',
                               'username':'',
                               'apodo':'',
                               'link':'',
                               'biografia':'',
                               'genero':'',
                               'fecha_nacimiento':''}, {'foto':'', 'banner':''}, instance = self.user)
        self.assertFalse(form.is_valid())

