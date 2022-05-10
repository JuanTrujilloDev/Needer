from allauth.socialaccount.views import SignupView
from allauth.account.views import SignupView
from .forms import SocialCustomForm, SignupCustomForm

class SocialUserSignupView(SignupView):
    # TODO AGREGAR EL GRUPO AL USUARIO
    # Segun el tipo de usuario se actualizaran los campos
    form_class = SocialCustomForm
    
class UserSignupView(SignupView):
    # TODO AGREGAR EL GRUPO AL USUARIO
    # Segun el tipo de usuario se actualizaran los campos
    form_class = SignupCustomForm
    

    
