from allauth.socialaccount.views import SignupView as SocialSignupView, ConnectionsView
from allauth.account.views import (SignupView, PasswordChangeView, EmailView,
                                   AccountInactiveView)
from django.views.generic import UpdateView
from .models import User
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.http import HttpResponseNotFound
from allauth.socialaccount.models import SocialAccount
from django.http import Http404
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Pais
from .forms import (SocialCustomForm, SignupCustomForm, UpdateUserForm)



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


class UpdateUserView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    UpdateCreador

    Vista para actualizar el usuario

    Attrs: Request, *args, **kwargs

    Returns: User Instance Updated
    """
    # TODO AGREGAR EL FORM Y VALIDAR CAMPOS
    success_message = 'Perfil actualizado satisfactoriamente!'
    model = User
    form_class = UpdateUserForm
    template_name = 'account/user/update-user.html'

    def get_success_url(self) -> str:
        return reverse('account_profile')

    def get_object(self):
        return User.objects.get(pk = self.request.user.id)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['pais'] = Pais.objects.all().order_by('nombre')
        context['socials'] = SocialAccount.objects.filter(user = self.get_object())

        return context




def updateAccountViewResolver(request):
    """
    updateAccountViewResolver

    Resolver el cual me retorna una vista dependiendo al grupo
    al cual pertenece el usuario.

    arguments: request

    returns: ClassBasedView.


    
    """


    if request.user.is_authenticated:

            return UpdateUserView.as_view()(request)



    else:
        return redirect(reverse('account_login'))





class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):

    def get_context_data(self, **kwargs):
        context = super(PasswordChangeView, self).get_context_data(**kwargs)
        context['base_template'] = 'main/user/content.html'

        return context

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated:

            if not self.request.user.is_active:

                return redirect(reverse('account_inactive'))
            
            return super(CustomPasswordChangeView, self).dispatch(request, *args, **kwargs)

            

        return redirect(reverse('account_login'))


class CustomEmailChangeView(LoginRequiredMixin, EmailView):

    def get_context_data(self, **kwargs):
        context = super(CustomEmailChangeView, self).get_context_data(**kwargs)
        context['base_template'] = 'main/user/content.html'

        return context

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated:

            if not self.request.user.is_active:

                return redirect(reverse('account_inactive'))
            
            return super(CustomEmailChangeView, self).dispatch(request, *args, **kwargs)

            

        return redirect(reverse('account_login'))



class CustomConnectionsView(LoginRequiredMixin, ConnectionsView):

    def get_context_data(self, **kwargs):
        context = super(CustomConnectionsView, self).get_context_data(**kwargs)
        context['base_template'] = 'main/user/content.html'


        return context

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated:

            if not self.request.user.is_active:

                return redirect(reverse('account_inactive'))
            
            return super(CustomConnectionsView, self).dispatch(request, *args, **kwargs)

            

        return redirect(reverse('account_login'))





# ACCOUNT INACTIVE VIEW
class CustomInactiveView(AccountInactiveView):

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated:

            if not request.user.is_active:

                return super(CustomInactiveView, self).dispatch(request, *args, **kwargs)

            return redirect(reverse('account_email'))

        return redirect(reverse('account_login'))


    
    
