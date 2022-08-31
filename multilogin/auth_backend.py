from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import OAuthToken
from .multilogin import get_user_info

User = get_user_model()


class MultiloginBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        if "auth_provider" in kwargs and "identifier" in kwargs:
            provider = kwargs["auth_provider"]
            identifier = kwargs["identifier"]
        elif "oauth" in request.session:
            provider = request.session["oauth"]["name"]
            userinfo = get_user_info(provider, token=request.session["oauth"])
            if not userinfo:
                return None
            identifier = userinfo.identifier
            request.session.pop("oauth", None)      # Remove the oauth stuff from the session
        else:
            return None
        try:
            token = OAuthToken.objects.get(
                provider=provider,
                identifier=identifier
            )
        except OAuthToken.DoesNotExist:
            return None
        return token.owner
