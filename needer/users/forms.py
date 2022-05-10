
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from allauth.account.forms import SignupForm as SignupForm
from allauth.socialaccount.adapter import get_adapter
from django import forms
from .models import User
import re
from .extras import numeros

class  SocialCustomForm(SocialSignupForm):
    first_name = forms.CharField(max_length=30, label="Nombres", required=True)
    last_name = forms.CharField(max_length=30, label="Apellidos", required=True)
    password1 = forms.CharField(max_length=30,label=("Contrasena"), widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(max_length=30, label=("Confirma tu contrasena"), widget=forms.PasswordInput, required=True)
    tipo_documento = forms.ChoiceField(choices = User.TipoDocumento.choices)
    num_documento = forms.CharField(max_length=10, label="Numero de documento")
    via = forms.CharField(max_length=10, label="Via")
    numero1 = forms.CharField(max_length=10, label="#")
    numero2 = forms.CharField(max_length=10, label="-", validators=[numeros]) 
    
    # TODO TIPO DE USUARIO CON AJAX
    # TODO CIUDAD Y DEPARTAMENTO CON AJAX VIEW
    # TODO CAPTCHA 
    

    #taken from https://github.com/pennersr/django-allauth/blob/master/allauth/account/forms.py

    def clean_password2(self):
        if ("password1" in self.cleaned_data and "password2" in self.cleaned_data):
            if (self.cleaned_data["password1"] != self.cleaned_data["password2"]):
                raise forms.ValidationError("Ambas contrasenas deben coincidir.")
        return self.cleaned_data["password2"]
    
    def clean_num_documento(self):
        """clean_num_documento

        Segun el tipo de documento que se escoja se deben llevar unos parametros.
        
        Nos devolvera error en caso de que no se cumplan estos.

        Returns:
            _type_: _description_
        """
        
        if (self.cleaned_data["tipo_documento"] == "CC"):
            match = re.match("[0-9]{8,10}", self.cleaned_data["num_documento"])
            
        elif (self.cleaned_data["tipo_documento"] == "CE"):
            match = re.match("[0-9]{6}", self.cleaned_data["num_documento"])
            
        elif (self.cleaned_data["tipo_documento"] == "PA"):
            match = re.match("[A-Za-z]{2}[0-9]{6}", self.cleaned_data["num_documento"])
            
        else:
            raise forms.ValidationError("Error en el tipo de documento.")
        
        if match:
            return self.cleaned_data["num_documento"]
        else:
            raise forms.ValidationError("Error en el numero de documento.")
            
        
    
    def save(self, request):
        """Save method actualizado

        Args:
            request (_type_): Post method.
            self (form): Recibe el formulario con los datos.
            
        Operations:
        
            Me agrega los campos adicionales que se requieren en el usuario.

        Returns:
            _type_: _description_
        """
        adapter = get_adapter(request)
        user = adapter.save_user(request, self.sociallogin, form=self)
        user.tipo_documento = self.cleaned_data["tipo_documento"]
        user.num_documento = self.cleaned_data["num_documento"]
        user.direccion_facturacion = "{} # {} - {}".format(self.cleaned_data["via"], self.cleaned_data["numero1"], self.cleaned_data["numero2"])
        user.save()
        self.custom_signup(request, user)
        return user
        
        
    def signup(self, request, user):
        user.set_password(self.user, self.cleaned_data["password1"])
        user.tipo_documento = self.cleaned_data["tipo_documento"]
        user.save()
        
        

class  SignupCustomForm(SignupForm):
    
    first_name = forms.CharField(max_length=30, label="Nombres", required=True)
    last_name = forms.CharField(max_length=30, label="Apellidos", required=True)
    password1 = forms.CharField(max_length=30,label=("Contrasena"), widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(max_length=30, label=("Confirma tu contrasena"), widget=forms.PasswordInput, required=True)
    tipo_documento = forms.ChoiceField(choices = User.TipoDocumento.choices)
    num_documento = forms.CharField(max_length=10, label="Numero de documento")
    via = forms.CharField(max_length=10, label="Via")
    numero1 = forms.CharField(max_length=10, label="#")
    numero2 = forms.CharField(max_length=10, label="-", validators=[numeros]) 
    
    # TODO CIUDAD Y DEPARTAMENTO CON AJAX VIEW
    
    # TODO TIPO DE USUARIO CON AJAX
    
    # TODO CAPTCHA 
    

    #taken from https://github.com/pennersr/django-allauth/blob/master/allauth/account/forms.py

    def clean_password2(self):
        if ("password1" in self.cleaned_data and "password2" in self.cleaned_data):
            if (self.cleaned_data["password1"] != self.cleaned_data["password2"]):
                raise forms.ValidationError("Ambas contrasenas deben coincidir.")
        return self.cleaned_data["password2"]
    
    def clean_num_documento(self):
        """clean_num_documento

        Segun el tipo de documento que se escoja se deben llevar unos parametros.
        
        Nos devolvera error en caso de que no se cumplan estos.

        Returns:
            _type_: _description_
        """
        
        if (self.cleaned_data["tipo_documento"] == "CC"):
            match = re.match("[0-9]{8,10}", self.cleaned_data["num_documento"])
            
        elif (self.cleaned_data["tipo_documento"] == "CE"):
            match = re.match("[0-9]{6}", self.cleaned_data["num_documento"])
            
        elif (self.cleaned_data["tipo_documento"] == "PA"):
            match = re.match("[A-Za-z]{2}[0-9]{6}", self.cleaned_data["num_documento"])
            
        else:
            raise forms.ValidationError("Error en el tipo de documento.")
        
        if match:
            return self.cleaned_data["num_documento"]
        else:
            raise forms.ValidationError("Error en el numero de documento.")
            
        
    
    def save(self, request= None):
        """Save method actualizado

        Args:
            request (_type_): Post method.
            self (form): Recibe el formulario con los datos.
            
        Operations:
        
            Me agrega los campos adicionales que se requieren en el usuario.

        Returns:
            _type_: _description_
        """
        user = super(SignupCustomForm, self).save(request)
        user.tipo_documento = self.cleaned_data["tipo_documento"]
        user.num_documento = self.cleaned_data["num_documento"]
        user.direccion_facturacion = "{} # {} - {}".format(self.cleaned_data["via"], self.cleaned_data["numero1"], self.cleaned_data["numero2"])
        user.save()
        return user
        
        
    def signup(self, request, user):
        user.set_password(self.user, self.cleaned_data["password1"])
        user.save()
    
        
        
        

