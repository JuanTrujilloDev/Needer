from allauth.socialaccount.views import SignupView as SocialSignupView
from allauth.account.views import SignupView
from .forms import SocialCustomForm, SignupCustomForm

class SocialUserSignupView(SocialSignupView):
    # Segun el tipo de usuario se actualizaran los campos
    form_class = SocialCustomForm
    
class UserSignupView(SignupView):
    # Segun el tipo de usuario se actualizaran los campos
    form_class = SignupCustomForm
    

    
