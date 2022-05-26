from unittest import TestProgram
from django.views.generic import TemplateView

# Create your views here.
class HomeView (TemplateView):
    template_name= "main/home.html"
    
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = 'Needer | Home'

        return context

    # TODO Los usuarios autenticados se les renvia al feed