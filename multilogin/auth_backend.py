from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import OAuthToken


User = get_user_model()


class MultiloginBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        if "auth_provider" not in kwargs or "identifier" not in kwargs:
            return None
        try:
            token = OAuthToken.objects.get(
                provider=kwargs["auth_provider"],
                identifier=kwargs["identifier"]
            )
        except OAuthToken.DoesNotExist:
            return None
        return token.owner
