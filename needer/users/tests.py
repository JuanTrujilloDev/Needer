from django.test import TestCase, Client
from .forms import SignupCustomForm
from .models import Pais, User
from django.urls import reverse
from django.conf import settings
from allauth.account.models import EmailAddress
from unittest.mock import patch
from captcha.client import RecaptchaResponse

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