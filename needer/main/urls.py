from django.urls import path, include
from .views import HomeView, AboutView, TerminosView, PoliticasView

urlpatterns = [
    
path('', HomeView.as_view(), name="home-view"),
path('about/', AboutView.as_view(), name="about-view"),
path('terminos/', TerminosView.as_view(), name="terminos-view"),
path('politicas/', PoliticasView.as_view(), name="politicas-view"),

]