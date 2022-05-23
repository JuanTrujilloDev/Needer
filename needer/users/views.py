from multiprocessing import get_context
from allauth.socialaccount.views import SignupView as SocialSignupView
from allauth.account.views import SignupView
from django.views.generic import UpdateView
from .models import User
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.http import HttpResponseNotFound


from .models import Pais
from .forms import SocialCustomForm, SignupCustomForm



# User CREATION VIEWS
class SocialUserSignupView(SocialSignupView):
    """
    SocialSignupView

    Vista para registrarse a traves de API.

    Arguments: Requests, *args, **kwargs

    Retorna: Instancia del usuario creado. / Redirect al login
    
    """
    form_class = SocialCustomForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pais"] = Pais.objects.all()
        return context
    
    
class UserSignupView(SignupView):
    """
    SignupView

    Vista para registrarse.

    Arguments: Requests, *args, **kwargs

    Retorna: Instancia del usuario creado. / Redirect al login
    
    """
    # Segun el tipo de usuario se actualizaran los campos
    form_class = SignupCustomForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pais"] = Pais.objects.all()
        return context



# User UPDATE VIEWS

class UpdateConsumidorView(UpdateView):
    """
    UpdateConsumidor

    Vista para actualizar el usuario que petenece
    al grupo consumidor.

    Arguments: Request, *args, **kwargs

    Returns: User Instance Updated
    """

    # TODO AGREGAR EL FORM Y VALIDAR CAMPOS
    model = User
    fields = ['email', 'username']
    template_name = 'account/consumidor/update-consumidor.html'

    def get_object(self):
        return User.objects.get(pk = self.request.user.id)


class UpdateCreadorView(UpdateView):
    """
    UpdateCreador

    Vista para actualizar el usuario que petenece
    al grupo creador de contenido.

    Attrs: Request, *args, **kwargs

    Returns: User Instance Updated
    """
    # TODO AGREGAR EL FORM Y VALIDAR CAMPOS
    model = User
    fields = ['first_name', 'last_name', 'num_documento', 'pais', 'username', 'email']
    template_name = 'account/creador/update-creador.html'

    def get_object(self):
        return User.objects.get(pk = self.request.user.id)


def updateAccountViewResolver(request):
    """
    updateAccountViewResolver

    Resolver el cual me retorna una vista dependiendo al grupo
    al cual pertenece el usuario.

    arguments: request

    returns: ClassBasedView.


    
    """


    if request.user.is_authenticated:

        if request.user.groups.name == 'Consumidor':
            return UpdateConsumidorView.as_view()(request)

        elif request.user.groups.name == 'Creador de Contenido':
            return UpdateCreadorView.as_view()(request)

        else:
            return HttpResponseNotFound('Not found')

    else:
        return redirect(reverse('account_login'))








    



# TODO En el login agregar el captcha.
    

    
