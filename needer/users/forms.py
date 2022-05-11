
from email.policy import default
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from allauth.account.forms import SignupForm as SignupForm
from allauth.socialaccount.adapter import get_adapter
from django import forms
from .models import User
from django.db.models import Q
from django.contrib.auth.models import Group
import re
from .extras import numeros

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
    
    
    first_name = forms.CharField(max_length=30, label="Nombres", required=True)
    last_name = forms.CharField(max_length=30, label="Apellidos", required=True)
    password1 = forms.CharField(max_length=30,label=("Contrasena"), widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(max_length=30, label=("Confirma tu contrasena"), widget=forms.PasswordInput, required=True)
    tipo_documento = forms.ChoiceField(choices = User.TipoDocumento.choices)
    num_documento = forms.CharField(max_length=10, label="Numero de documento")
    via = forms.CharField(max_length=10, label="Via")
    numero1 = forms.CharField(max_length=10, label="#")
    numero2 = forms.CharField(max_length=10, label="-", validators=[numeros]) 
    groups = forms.ModelChoiceField(queryset = Group.objects.filter(Q(name="Consumidor") | Q(name = "Creador de Contenido")), blank=False, required=True)
    
    # TODO NUMERO DE CELULAR
    # TODO CIUDAD Y DEPARTAMENTO CON AJAX VIEW
    # TODO CAPTCHA 
    
    def __init__(self, *args, **kwargs):
        # Haciendo que el correo que se trae del API no se pueda tocar en el FORM!
        super(SocialCustomForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['readonly'] = True
        
    

    #taken from https://github.com/pennersr/django-allauth/blob/master/allauth/account/forms.py

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
        
        if (self.cleaned_data["tipo_documento"] == "CC"):
            match = re.match("[0-9]{8,10}", self.cleaned_data["num_documento"])
            
        elif (self.cleaned_data["tipo_documento"] == "CE"):
            match = re.match("[0-9]{6}", self.cleaned_data["num_documento"])
            
        elif (self.cleaned_data["tipo_documento"] == "PA"):
            match = re.match("[A-Za-z]{2}[0-9]{6}", self.cleaned_data["num_documento"])
            
        else:
            raise forms.ValidationError("Error en el tipo de documento.")
        
        if match:
            # Me genera ruido el numero de doc repetido
            if not User.objects.filter(num_documento = self.cleaned_data["num_documento"]):
                return self.cleaned_data["num_documento"]
            
            else:
                raise forms.ValidationError("Ya hay un usuario registrado con este numero de documento!")   
        else:
            raise forms.ValidationError("Error en el numero de documento.")
            
        
    
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
        user.tipo_documento = self.cleaned_data["tipo_documento"]
        user.num_documento = self.cleaned_data["num_documento"]
        user.direccion_facturacion = "{} # {} - {}".format(self.cleaned_data["via"], self.cleaned_data["numero1"], self.cleaned_data["numero2"])
        user.groups = self.cleaned_data["groups"]
        user.save()
        self.custom_signup(request, user)
        return user
        
        
    def signup(self, request, user):
        user.set_password(self.user, self.cleaned_data["password1"])
        user.tipo_documento = self.cleaned_data["tipo_documento"]
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
    
    first_name = forms.CharField(max_length=30, label="Nombres", required=True)
    last_name = forms.CharField(max_length=30, label="Apellidos", required=True)
    password1 = forms.CharField(max_length=30,label=("Contrasena"), widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(max_length=30, label=("Confirma tu contrasena"), widget=forms.PasswordInput, required=True)
    tipo_documento = forms.ChoiceField(choices = User.TipoDocumento.choices)
    num_documento = forms.CharField(max_length=10, label="Numero de documento")
    via = forms.CharField(max_length=10, label="Via")
    numero1 = forms.CharField(max_length=10, label="#")
    numero2 = forms.CharField(max_length=10, label="-", validators=[numeros]) 
    groups = forms.ModelChoiceField(queryset = Group.objects.filter(Q(name="Consumidor") | Q(name = "Creador de Contenido")), label="Tipo de Usuario", blank=False, required=True)
    
    # TODO CIUDAD Y DEPARTAMENTO CON AJAX VIEW
    # TODO NUMERO DE CELULAR
    
    # TODO CAPTCHA 
    

    #taken from https://github.com/pennersr/django-allauth/blob/master/allauth/account/forms.py

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
        
        if (self.cleaned_data["tipo_documento"] == "CC"):
            match = re.match("[0-9]{8,10}", self.cleaned_data["num_documento"])
            
        elif (self.cleaned_data["tipo_documento"] == "CE"):
            match = re.match("[0-9]{6}", self.cleaned_data["num_documento"])
            
        elif (self.cleaned_data["tipo_documento"] == "PA"):
            match = re.match("[A-Za-z]{2}[0-9]{6}", self.cleaned_data["num_documento"])
            
        else:
            raise forms.ValidationError("Error en el tipo de documento.")
        
        if match:
            # Me genera ruido el numero de doc repetido
            if not User.objects.filter(num_documento = self.cleaned_data["num_documento"]):
                return self.cleaned_data["num_documento"]
            
            else:
                raise forms.ValidationError("Ya hay un usuario registrado con este numero de documento!")   
        else:
            raise forms.ValidationError("Error en el numero de documento.")
            
        
    
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
        user.tipo_documento = self.cleaned_data["tipo_documento"]
        user.num_documento = self.cleaned_data["num_documento"]
        user.direccion_facturacion = "{} # {} - {}".format(self.cleaned_data["via"], self.cleaned_data["numero1"], self.cleaned_data["numero2"])
        user.groups = self.cleaned_data["groups"]
        user.save()
        return user
        
        
    def signup(self, request, user):
        user.set_password(self.user, self.cleaned_data["password1"])
        user.save()
    
        
        
        

