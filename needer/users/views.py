from multiprocessing import get_context
from allauth.socialaccount.views import SignupView as SocialSignupView
from allauth.account.views import SignupView

from .models import Pais
from .forms import SocialCustomForm, SignupCustomForm

class SocialUserSignupView(SocialSignupView):
    # Segun el tipo de usuario se actualizaran los campos
    form_class = SocialCustomForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pais"] = Pais.objects.all()
        return context
    
    
class UserSignupView(SignupView):
    # Segun el tipo de usuario se actualizaran los campos
    form_class = SignupCustomForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pais"] = Pais.objects.all()
        return context



# TODO En el login agregar el captcha.
    

    
