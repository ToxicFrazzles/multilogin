from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.utils.timezone import datetime
from authlib.integrations.django_client import token_update


class DiscordLogin(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    discord_id = models.CharField(max_length=32, unique=True, db_index=True)
    access_token = models.CharField(max_length=256)
    refresh_token = models.CharField(max_length=256)
    expires = models.DateTimeField()

    def to_token(self):
        return {
            "access_token": self.access_token,
            "token_type": "Bearer",
            "refresh_token": self.refresh_token,
            "expires_at": self.expires.timestamp()
        }


@receiver(token_update)
def on_token_update(sender, name, token, refresh_token=None, access_token=None, **kwargs):
    print("Token updated!")
    if name != "discord":
        return
    print("It's a discord token!")
    if refresh_token:
        item = DiscordLogin.objects.get(refresh_token=refresh_token)
    elif access_token:
        item = DiscordLogin.objects.get(access_token=access_token)
    else:
        return
    item.access_token = token["access_token"]
    item.refresh_token = token["refresh_token"]
    item.expires = datetime.fromtimestamp(token["expires_at"])
    item.save()
