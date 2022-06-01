from django.db.models.signals import pre_save, m2m_changed
from django.dispatch import receiver
from .models import Publicacion
from django.utils.text import slugify
from django.core.exceptions import ValidationError



