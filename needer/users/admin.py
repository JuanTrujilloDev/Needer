from django.contrib import admin
from .models import TipoCelebridad, User, Pais

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    pass

admin.site.register(Pais)
admin.site.register(User, UserAdmin)
admin.site.register(TipoCelebridad)
