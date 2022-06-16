from django.shortcuts import render, redirect
from django.views.generic import DetailView, CreateView, ListView
from users.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth import logout
from .models import Publicacion
from django.http import HttpResponseNotFound
from .forms import CrearPublicacionForm
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator




# VISTA PARA PERFIL DEL CREADOR DE CONTENIDO
class DetailCreador(LoginRequiredMixin, ListView):
    model = Publicacion
    template_name = 'social/user/perfil.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context['object'] = User.objects.get(slug = self.kwargs['slug'])
        context['innercontent'] = 'main/user/content.html'

        return context

    def get_queryset(self, **kwargs):
        user = User.objects.get(slug = self.kwargs['slug'])
        return Publicacion.objects.filter(user = user).order_by('-fecha_creacion')


    def get_template_names(self):
        return ['social/user/perfil.html']
            

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.is_active:
                    return super().dispatch(request, *args, **kwargs)
            else:
                logout(self.request)
                return redirect(reverse('account_inactive'))
        else:
            return redirect(reverse('account_login'))




# CRUD PUBLICACIONES

class CrearPublicacionView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Publicacion
    template_name = 'social/user/crear-publi.html'
    form_class = CrearPublicacionForm
    success_message = 'La publicacion fue creada satisfactoriamente!'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.is_active:
                # Lo envia a crear la publicacion
                return super().dispatch(request, *args, **kwargs)


            else:
                logout(self.request)
                return redirect(reverse('account_inactive'))
        else:
            return redirect(reverse('account_login'))

    # Se sobrescribe el form_valid para guardar el autor.
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        return redirect(self.get_success_url())

    def get_success_url(self) -> str:
        return reverse('detalle-publicacion', kwargs={'pk': self.object.pk, 'user_slug': self.object.user.slug})


class DetallePublicacionView(LoginRequiredMixin, DetailView):
    model = Publicacion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_slug'] = self.get_object().user.slug

        context['innercontent'] = 'main/user/content.html'

        return context


    def get_template_names(self):
            return ['social/user/detalle-publicacion.html']
            

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.is_active:
                # Si el usuario es consumidor o es el dueno del perfil
                return super().dispatch(request, *args, **kwargs)

            else:
                logout(self.request)
                return redirect(reverse('account_inactive'))
        else:
            return redirect(reverse('account_login'))
