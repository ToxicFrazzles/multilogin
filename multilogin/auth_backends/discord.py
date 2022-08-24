from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from ..models.discord_login import DiscordLogin


User = get_user_model()


class DiscordLoginBackend(BaseBackend):
    def authenticate(self, request, **kwargs):
        if "discord_user_id" not in kwargs:
            return None
        try:
            user = DiscordLogin.objects.get(discord_id=kwargs["discord_user_id"]).user
        except DiscordLogin.DoesNotExist:
            return None
        return user

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        return user

