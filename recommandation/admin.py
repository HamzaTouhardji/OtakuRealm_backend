from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Anime, Genre, Utilisateur, Preferer, Review, Recommandation

# Define an inline admin descriptor for Utilisateur model
# which acts a bit like a singleton
class UtilisateurInline(admin.StackedInline):
    model = Utilisateur
    can_delete = False
    verbose_name_plural = 'utilisateur'

# Define a new Utilisateur admin
class UserAdmin(BaseUserAdmin):
    inlines = (UtilisateurInline,)

admin.site.register(Anime)
admin.site.register(Genre)
admin.site.register(Utilisateur)
admin.site.register(Preferer)
admin.site.register(Review)
admin.site.register(Recommandation)