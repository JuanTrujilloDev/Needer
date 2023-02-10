from tkinter import Widget
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from allauth.account.forms import SignupForm as SignupForm
from allauth.account.forms import ResetPasswordForm
from allauth.socialaccount.adapter import get_adapter
from django import forms
from .models import TipoCelebridad, User, Pais
from django.db.models import Q
from django.contrib.auth.models import Group
import re
from .extras import numeros
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from datetime import date
from django.forms import URLField
from django.core.exceptions import ValidationError



class CustomResetPasswordForm(ResetPasswordForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3)



class  SocialCustomForm(SocialSignupForm):
    """ SOCIAL CUSTOM FORM

    Args:
        SocialSignupForm (FORM): Hereda de SocialSignupForm de ALLAUTH

    Execution:
            Recibe los parametros del USER
             
            El campo email es readonly para que no se pueda modificar.
            Ya que se recibe de la API
            

    Returns:
        OBJ: El usuario creado por el metodo save()
    """
    
 
    first_name = forms.CharField(max_length=30, label="Nombres", required=False)
    last_name = forms.CharField(max_length=30, label="Apellidos", required=False)
    password1 = forms.CharField(max_length=30,label=("Contrasena"), widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(max_length=30, label=("Confirma tu contrasena"), widget=forms.PasswordInput, required=True)
    pais = forms.CharField(max_length=50, required=False)
    num_documento = forms.CharField(max_length=10, label="Numero de documento", required=False)
    """     via = forms.CharField(max_length=10, label="Via")
    numero1 = forms.CharField(max_length=10, label="#")
    numero2 = forms.CharField(max_length=10, label="-", validators=[numeros]) 
    zip = forms.CharField(max_length=9, label="Zip Code", validators=[numeros]) """
    captcha = ReCaptchaField(widget=ReCaptchaV3, label="", required=True)
   
   
   
    # TODO NUMERO DE CELULAR
    
    
    def __init__(self, *args, **kwargs):
        # Haciendo que el correo que se trae del API no se pueda tocar en el FORM!
        super(SocialCustomForm, self).__init__(*args, **kwargs)
        self.fields['pais'].widget.attrs['list'] = 'id_pais'
        self.fields['email'].widget.attrs['readonly'] = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = "form-control"
        
    

    # Validar campos
    def clean(self):
        """
        Validate the form input
        """
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        num_documento = cleaned_data.get('num_documento')
        pais = cleaned_data.get('pais')

        if first_name == "":
            self.add_error('first_name', ("Este campo es obligatorio")) 
        else:
            match = re.match('^[A-Z][a-zA-Z ]+$', first_name)

            if match:
                pass
            else:
                self.add_error('first_name', ('Formato Invalido. El nombre debe contener solo letras y empezar por mayuscula.'))

        if last_name == "":
            self.add_error('last_name', ("Este campo es obligatorio")) 
        else:
            if match:
                pass
            else:
                self.add_error('last_name', ('Formato Invalido. El apellido debe contener solo letras y empezar por mayuscula.'))

        if num_documento == "":
            self.add_error('num_documento', ("Este campo es obligatorio")) 

        if pais == "":
            self.add_error('pais', ("Este campo es obligatorio")) 

        return cleaned_data

    #taken from https://github.com/pennersr/django-allauth/blob/master/allauth/account/forms.py

    def clean_username(self):
        """
        Se limpia el usuario para cumplir con el formato

        3 a 18 Caracteres
        Solo Letras [A-Za-z numeros o ._]
        """
        username = self.cleaned_data['username']
        
        # Regex para nombre de usuario 

        match = re.match('^[A-Za-z][A-Za-z0-9]{3,18}$', username)

        if match:
            if username.lower() in ['home', 'marketplace', 'signup', 'logout', 'email', 'inactive', 'follow', 'unfollow', 'profile', 'chat']:
                raise forms.ValidationError('No puedes usar este nombre de usuario')

            try:
                persona = User.objects.get(username__iexact=username)
            except:
                return username

            if persona:
                raise forms.ValidationError('El nombre de usuario ya se encuentra registrado, intenta con otro.')

        raise forms.ValidationError('El usuario no cumple con el formato (Solo letras o numeros y debe empezar por letra) de 3 a 18 caracteres.')





    def clean_password2(self):
        """clean_password2
        
        Raises:
            forms.ValidationError: En caso de que las contrasenas no coincidan

        Returns:
            String(Formatted): Retorna las contrasenas y las almacena en caso de 
            que si coincidan y cumplan los parametros.
                    
                    
        """
        
        if ("password1" in self.cleaned_data and "password2" in self.cleaned_data):
            if (self.cleaned_data["password1"] != self.cleaned_data["password2"]):
                raise forms.ValidationError("Ambas contrasenas deben coincidir.")
        return self.cleaned_data["password2"]
    

    def clean_num_documento(self):
        """clean_num_documento

        Segun el tipo de documento que se escoja se deben llevar unos parametros.
        
        Nos devolvera error en caso de que no se cumplan estos.

        Returns:
            String: num_documento
        """
        # TODO POSIBLEMENTE AGREGAR ERROR PARA DAR PISTA A CADA TIPO DE DOCUMENTO
        # EJ: ERROR EN EL NUMERO DE CEDULA EL FORMATO ES (12345678 o 1234567890)        

        match = re.match("[0-9]{6,10}", self.cleaned_data["num_documento"])
        
        
        if match:
            # Me genera ruido el numero de doc repetido
            if not User.objects.filter(num_documento = self.cleaned_data["num_documento"]):
                return self.cleaned_data["num_documento"]
            
            else:
                raise forms.ValidationError("Ya hay un usuario registrado con este numero de documento!")   
        else:
            raise forms.ValidationError("Error en el numero de documento debe contener solo numeros (De 6 - 10 numeros).")
        
        
    def clean_pais(self):
        pais = self.cleaned_data['pais']
        try:
            paises = Pais.objects.get(nombre = pais)
        except:
            raise forms.ValidationError('El pais no se encuentra en la lista')

        return paises

            
        
    
    def save(self, request):
        """Save method actualizado

        Args:
            request (POST): Post method.
            self (form): Recibe el formulario con los datos.
            
        Operations:
        
            Me agrega los campos adicionales que se requieren en el usuario.

        Returns:
            Obj: User
        """
        
        adapter = get_adapter(request)
        user = adapter.save_user(request, self.sociallogin, form=self)
        user.num_documento = self.cleaned_data["num_documento"]
        #user.direccion_facturacion = "{} # {} - {}, {}".format(self.cleaned_data["via"], self.cleaned_data["numero1"], self.cleaned_data["numero2"], self.cleaned_data["zip"])
        user.pais = self.cleaned_data["pais"]
        user.save()
        self.custom_signup(request, user)
        return user
        
        
    def signup(self, request, user):
        user.set_password(self.user, self.cleaned_data["password1"])
        user.save()
        
        

class  SignupCustomForm(SignupForm):
    
    """SignupCustomForm
    
    Arguments: Hereda del SignupForm base de allauth.
    

    Execution:
               Recibe todos los campos de usuario.
               En el front se eliminan o se esconden segun la necesidad.

    Returns:
        OBJ: La instancia guardada del usuario y la redireccion.
    """
    
    first_name = forms.CharField(max_length=30, label="Nombres", required=False)
    last_name = forms.CharField(max_length=30, label="Apellidos", required=False)
    password1 = forms.CharField(max_length=30,label=("Contrasena"), widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(max_length=30, label=("Confirma tu contrasena"), widget=forms.PasswordInput, required=True)
    pais = forms.CharField(max_length=50, required=False)
    num_documento = forms.CharField(max_length=10, label="Numero de documento", required=False)
    """     via = forms.CharField(max_length=10, label="Via")
    numero1 = forms.CharField(max_length=10, label="#")
    numero2 = forms.CharField(max_length=10, label="-", validators=[numeros]) 
    zip = forms.CharField(max_length=9, label="Zip Code", validators=[numeros]) """
    captcha = ReCaptchaField(widget=ReCaptchaV3, label="", required=True)
   
    
    # TODO NUMERO DE CELULAR
    # TODO Username | Nickname
    
    def __init__(self, *args, **kwargs):
        # Haciendo que el correo que se trae del API no se pueda tocar en el FORM!
        super(SignupCustomForm, self).__init__(*args, **kwargs)
        self.fields['pais'].widget.attrs['list'] = 'id_pais'
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = "form-control"

    #taken from https://github.com/pennersr/django-allauth/blob/master/allauth/account/forms.py


    # Validar campos
    def clean(self):
        """
        Validate the form input
        """
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        num_documento = cleaned_data.get('num_documento')
        pais = cleaned_data.get('pais')

        if first_name == "":
            self.add_error('first_name', ("Este campo es obligatorio")) 
        else:
            match = re.match('^[A-Z][a-zA-Z ]+$', first_name)

            if match:
                pass
            else:
                self.add_error('first_name', ('Formato Invalido. El nombre debe contener solo letras y empezar por mayuscula.'))

        if last_name == "":
            self.add_error('last_name', ("Este campo es obligatorio")) 
        else:
            if match:
                pass
            else:
                self.add_error('last_name', ('Formato Invalido. El apellido debe contener solo letras y empezar por mayuscula.'))

        if num_documento == "":
            self.add_error('num_documento', ("Este campo es obligatorio")) 

        if pais == "":
            self.add_error('pais', ("Este campo es obligatorio")) 

        return cleaned_data







        

    def clean_username(self):
        """
        Se limpia el usuario para cumplir con el formato

        3 a 18 Caracteres
        Solo Letras [A-Za-z numeros]
        """
        username = self.cleaned_data['username']

        # Regex para Username
        match = re.match('^[A-Za-z][A-Za-z0-9]{3,18}$', username)

        if match:
            if username.lower() in ['home', 'marketplace']:
                raise forms.ValidationError('No puedes usar este nombre de usuario')

            try:
                persona = User.objects.get(username__iexact=username)
            except:
                return username

            if persona:
                raise forms.ValidationError('El nombre de usuario ya se encuentra registrado, intenta con otro.')


        raise forms.ValidationError('El usuario no cumple con el formato (Solo letras o numeros y debe empezar por letra) de 3 a 18 caracteres.')




    def clean_password2(self):
        
        """clean_password2
        
        Raises:
            forms.ValidationError: En caso de que las contrasenas no coincidan

        Returns:
        
        String(formatted): Retorna las contrasenas y las almacena en caso de que si coincidan
                            y cumplan los parametros.
                    
                    
        """
        
        if ("password1" in self.cleaned_data and "password2" in self.cleaned_data):
            if (self.cleaned_data["password1"] != self.cleaned_data["password2"]):
                raise forms.ValidationError("Ambas contrasenas deben coincidir.")
        return self.cleaned_data["password2"]

    
    def clean_num_documento(self):
        """clean_num_documento

        Segun el tipo de documento que se escoja se deben llevar unos parametros.
        
        Nos devolvera error en caso de que no se cumplan estos.
        
        Adicionalmente si hay numero de documento repetido se dara otro error.

        Returns:
            String: numero de documento
        """
        # TODO POSIBLEMENTE AGREGAR ERROR PARA DAR PISTA A CADA TIPO DE DOCUMENTO
        # EJ: ERROR EN EL NUMERO DE CEDULA EL FORMATO ES (12345678 o 1234567890)


        match = re.match("[0-9]{6,10}", self.cleaned_data["num_documento"])
        
        
        if match:
            # Me genera ruido el numero de doc repetido
            if not User.objects.filter(num_documento = self.cleaned_data["num_documento"]):
                return self.cleaned_data["num_documento"]
            
            else:
                raise forms.ValidationError("Ya hay un usuario registrado con este numero de documento!")   
        else:
            raise forms.ValidationError("Error en el numero de documento debe contener solo numeros (De 6 - 10 numeros).")
        
        
    def clean_pais(self):
        
        pais = self.cleaned_data['pais']
        try:
            paises = Pais.objects.get(nombre = pais)
        except:
            raise forms.ValidationError('El pais no se encuentra en la lista')

        return paises


        
    
    def save(self, request= None):
        """Save method actualizado

        Args:
            request (POST): Post method.
            self (form): Recibe el formulario con los datos.
            
        Operations:
        
            Me agrega los campos adicionales que se requieren en el usuario.

        Returns:
            OBJ: User
        """
        user = super(SignupCustomForm, self).save(request)
        user.num_documento = self.cleaned_data["num_documento"]
        #user.direccion_facturacion = "{} # {} - {}, {}".format(self.cleaned_data["via"], self.cleaned_data["numero1"], self.cleaned_data["numero2"], self.cleaned_data["zip"])
        user.pais = self.cleaned_data["pais"]
        user.save()
        return user
        
        
    def signup(self, request, user):
        user.set_password(self.user, self.cleaned_data["password1"])
        user.save()




    

# FORM UPDATECREADOR
class UpdateUserForm(forms.ModelForm):

    # Fields
    first_name = forms.CharField(max_length=25, required=True, widget= forms.TextInput(attrs={'placeholder':'Ingresa tus nombres'}))
    last_name = forms.CharField(max_length=25, required=True, widget= forms.TextInput(attrs={'placeholder':'Ingresa tus apellidos'}))
    pais = forms.CharField(max_length=30, required=True, widget= forms.TextInput(attrs={'placeholder':'Ingresa tu pais de residencia'}))
    foto = forms.ImageField(required=False)
    fecha_nacimiento = forms.DateField(widget= forms.DateInput(attrs={'type': 'date'}), required=True)
    biografia = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder':'Cuentale a tu publico de ti... (Maximo 150 caracteres)',
    'onKeyUp':"maximo(this,150);", 'onKeyDown':"maximo(this,150);", 'onkeypress':"cancelar();"}))
    tipo_celebridad = forms.ModelMultipleChoiceField(queryset = TipoCelebridad.objects.all(), required = False, widget= forms.CheckboxSelectMultiple())
    banner = forms.ImageField(required=False)

    class Meta:
        # Model class
        model = User
        fields = ['first_name', 'last_name', 'pais', 'username', 'apodo', 'fecha_nacimiento', 
                 'genero', 'tipo_celebridad', 'foto', 'biografia', 'link', 'banner']


    #Constructor permite modificar los campos 
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        kwargs.update(initial={
            'pais':instance.pais.nombre
           
        })

        if instance.fecha_nacimiento:
             kwargs.update(initial={
            'fecha_nacimiento': instance.fecha_nacimiento.strftime("%Y-%m-%d"),
            'pais':instance.pais.nombre
           
            })
                
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.fields['pais'].widget.attrs['list'] = "id_pais"
        #self.fields['biografia'].widget.attrs['wrap'] = 'hard'
        

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Ingresa tu nombre'
        self.fields['first_name'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['last_name'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Ingresa tu apellido'
        self.fields['tipo_celebridad'].widget.attrs['class'] = 'form-check'
        

    def clean_biografia(self):
        #Eliminando los saltos de linea porque me cagan
        a = self.cleaned_data['biografia']
        _ = " ".join(a.split()[::])

        if len(_) > 150:
            raise forms.ValidationError('El maximo de caracteres es de 150')
        return _

    def clean_link(self):

        link = self.cleaned_data['link']

        url_form_field = URLField()
        # Se le agrega el if para que no valide si el link va vacio
        if link:
            try:
                url = url_form_field.clean(link)
            except ValidationError:
                raise forms.ValidationError('Ingrese un link valido')
        return link
        
    # clean methods

    # clean_first name
    def clean_first_name(self):

        first_name = self.cleaned_data['first_name']
        match = re.match('^[A-Z][a-zA-Z ]+$', first_name)

        if match:
            return first_name
            
        raise forms.ValidationError('Formato Invalido. El nombre debe contener solo letras y empezar por mayuscula.')

    # clean_last name
    def clean_last_name(self):

        last_name = self.cleaned_data['last_name']
        match = re.match('^[A-Z][a-zA-Z ]+$', last_name)

        if match:
            return last_name
            
        raise forms.ValidationError('Formato Invalido. El nombre debe contener solo letras y empezar por mayuscula.')
        


    
    def clean_pais(self):
        """En caso de que el usuario sea tipo consumidor se le asigna un pais predeterminado
        en este caso es United States of America, pero si es creador de contendio si se le
        permite especificar un pais""" 

        pais = self.cleaned_data['pais']
        try:
            paises = Pais.objects.get(nombre = pais)
        except:
            raise forms.ValidationError('El pais no se encuentra en la lista')

        return paises


    def clean_username(self):
        """
        Se limpia el usuario para cumplir con el formato

        3 a 18 Caracteres
        Solo Letras [A-Za-z numeros]
        """
        username = self.cleaned_data['username']

        # Regex para Username
        match = re.match('^[A-Za-z][A-Za-z0-9]{3,18}$', username)

        if match:
            if username.lower() in ['home', 'marketplace']:
                raise forms.ValidationError('No puedes usar este nombre de usuario')
            
            
            try:
                persona = User.objects.get(username__iexact=username)
            except:
                return username

            if persona and (self.instance != persona):
                raise forms.ValidationError('El nombre de usuario ya se encuentra registrado, intenta con otro.')
            
           
            
            else:
                return username


        raise forms.ValidationError('El usuario no cumple con el formato: De 4 a 10 caracteres (Solo letras o numeros y debe empezar por letra) de 3 a 18 caracteres.')

    def clean_apodo(self):
        """
        Se limpia el usuario para cumplir con el formato

        4 a 25 Caracteres
        Solo Letras [A-Za-z numeros]
        """
        apodo = self.cleaned_data['apodo']
        
        if apodo:
            

            # Regex para Username
            match = re.match('^[A-Za-z][A-Za-z0-9 ]{4,25}$', apodo)

            if match:
                    return apodo


            raise forms.ValidationError('El apodo no cumple con el formato (Solo letras, numeros o espacio y debe empezar por letra) minimo 4 caracteres y maximo 25 caracteres.')
        
        return apodo


    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data['fecha_nacimiento'].strftime('%Y')
        today = date.today().strftime('%Y')

        try:
            today = int(today)
            fecha = int(fecha)
        except:
            raise forms.ValidationError("Formato de fecha invalido.")

        else:
            if today-fecha < 18:
                
                raise forms.ValidationError("Debes tener al menos 18 para estar en la plataforma.")

            elif today-fecha >= 120:

                raise forms.ValidationError("Formato de fecha invalido.")

        
        return self.cleaned_data['fecha_nacimiento']

    #Funcion para validar la cantidad de categorias que puede eleguir 
    def clean_tipo_celebridad(self):

        categorias = self.cleaned_data['tipo_celebridad']

        if len(categorias) > 5:
            raise forms.ValidationError("No puedes escoger mas de 5 categorias, selecciona las que mas se ajusten a tu perfil.")

        return categorias



    
















    
        
        
        

