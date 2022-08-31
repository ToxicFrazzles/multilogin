from django.contrib import admin
from .models import OAuthToken


@admin.register(OAuthToken)
class OAuthTokenAdmin(admin.ModelAdmin):
    pass
