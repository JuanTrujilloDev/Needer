from django.contrib import admin
from .models import User, Pais

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    pass

admin.site.register(Pais)
admin.site.register(User, UserAdmin)
