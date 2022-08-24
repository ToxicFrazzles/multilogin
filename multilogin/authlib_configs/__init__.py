from authlib.integrations.django_client import OAuth
from django.conf import settings
from .discord import Discord

oauth = OAuth()

if getattr(settings, "DISCORD_CLIENT_ID", None) and getattr(settings, "DISCORD_CLIENT_SECRET", None):
    Discord.OAUTH_CONFIG.update(
        client_id=getattr(settings, "DISCORD_CLIENT_ID", None),
        client_secret=getattr(settings, "DISCORD_CLIENT_SECRET", None)
    )
    oauth.register(Discord.NAME, False, **Discord.OAUTH_CONFIG)
