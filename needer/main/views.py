from unittest import TestProgram
from django.views.generic import TemplateView
from django.urls import reverse
from django.shortcuts import redirect

# Create your views here.
class HomeView (TemplateView):
    template_name= "main/home.html"
    
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = 'Needer | Home'

        return context



    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('social-home'))

        return super().get(request, *args, **kwargs)


class AboutView (TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = 'Needer | About'

        return context



    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('social-home'))

        return super().get(request, *args, **kwargs)

class PoliticasView (TemplateView):
    template_name = 'main/politicas.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = 'Needer | Politicas de Privacidad'

        return context



    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('social-home'))

        return super().get(request, *args, **kwargs)


class TerminosView (TemplateView):
    template_name = 'main/terminos.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = 'Needer | Terminos y Condiciones'

        return context



    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('social-home'))

        return super().get(request, *args, **kwargs)