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
from .forms import (SocialCustomForm, SignupCustomForm, UpdateCreadorForm,
                    UpdateConsumidorForm)



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

class UpdateConsumidorView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    UpdateConsumidor

    Vista para actualizar el usuario que petenece
    al grupo consumidor.

    Arguments: Request, *args, **kwargs

    Returns: User Instance Updated
    """

    success_message = 'Perfil actualizado satisfactoriamente!'
    model = User
    form_class = UpdateConsumidorForm
    template_name = 'account/consumidor/update-consumidor.html'

    def get_object(self):
        return User.objects.get(pk = self.request.user.id)

    def get_success_url(self) -> str:
        return reverse('account_profile')

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['socials'] = SocialAccount.objects.filter(user = self.get_object())

        return context


class UpdateCreadorView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    UpdateCreador

    Vista para actualizar el usuario que petenece
    al grupo creador de contenido.

    Attrs: Request, *args, **kwargs

    Returns: User Instance Updated
    """
    # TODO AGREGAR EL FORM Y VALIDAR CAMPOS
    success_message = 'Perfil actualizado satisfactoriamente!'
    model = User
    form_class = UpdateCreadorForm
    template_name = 'account/creador/update-creador.html'

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

        if request.user.groups.name == 'Consumidor':
            return UpdateConsumidorView.as_view()(request)

        elif request.user.groups.name == 'Creador de Contenido':
            return UpdateCreadorView.as_view()(request)

        else:
            return HttpResponseNotFound('Not found')

    else:
        return redirect(reverse('account_login'))





class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):

    def get_context_data(self, **kwargs):
        context = super(PasswordChangeView, self).get_context_data(**kwargs)
        if self.request.user.groups.name == "Consumidor":
            context['base_template'] = 'main/consumidor/content-consumidor.html'
        elif self.request.user.groups.name == "Creador de Contenido":
            context['base_template'] = 'main/creador/content-creador.html'
        else:
            raise Http404

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
        if self.request.user.groups.name == "Consumidor":
            context['base_template'] = 'main/consumidor/content-consumidor.html'
        elif self.request.user.groups.name == "Creador de Contenido":
            context['base_template'] = 'main/creador/content-creador.html'
        else:
            raise Http404

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
        if self.request.user.groups.name == "Consumidor":
            context['base_template'] = 'main/consumidor/content-consumidor.html'
        elif self.request.user.groups.name == "Creador de Contenido":
            context['base_template'] = 'main/creador/content-creador.html'
        else:
            raise Http404

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


    
    
