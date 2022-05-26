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
            return redirect(reverse('account_profile'))

        return super().get(request, *args, **kwargs)