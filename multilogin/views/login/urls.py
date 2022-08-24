from django.urls import path
from django.conf import settings
from .discord import DiscordLoginView, DiscordRedirectView

urlpatterns = []

if "multilogin.auth_backends.discord.DiscordLoginBackend" in settings.AUTHENTICATION_BACKENDS \
        and getattr(settings, "DISCORD_CLIENT_ID", None) \
        and getattr(settings, "DISCORD_CLIENT_SECRET", None):
    urlpatterns += [
        path('discord/', DiscordLoginView.as_view(), name="discord"),
        path('discord/redirect/', DiscordRedirectView.as_view(), name="discord_redirect"),
    ]
