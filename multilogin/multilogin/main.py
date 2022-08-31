from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.timezone import datetime
from authlib.integrations.django_client import OAuth
from multilogin.models import OAuthToken
from . import backends


available_backends = [
    backends.Discord
]


User = get_user_model()


def fetch_token(name, request):
    if request.user.is_authenticated:
        try:
            token = OAuthToken.objects.get(
                provider=name,
                owner=request.user
            )
            return token.to_token()
        except OAuthToken.DoesNotExist:
            return None
    elif "oauth" in request.session and request.session["oauth"]["name"] == name:
        token = request.session.get("oauth")
        token.pop('name', None)
        return token


oauth = OAuth(fetch_token=fetch_token)


def enabled_backends():
    for backend in available_backends:
        client_id = getattr(settings, f"{backend.NAME.upper()}_CLIENT_ID", None)
        client_secret = getattr(settings, f"{backend.NAME.upper()}_CLIENT_SECRET", None)
        if client_id is not None and client_secret is not None:
            yield backend


def get_user_info(name, **kwargs):
    remote = oauth.create_client(name)
    backend = next((i for i in available_backends if i.NAME == name), None)
    resp = remote.get(backend.OAUTH_CONFIG['userinfo_endpoint'], **kwargs)
    resp.raise_for_status()
    return backend.OAUTH_CONFIG['userinfo_compliance_fix'](remote, resp.json())


def register_user(request, **kwargs):
    if "token" in kwargs and "backend" in kwargs:
        token = kwargs.pop("token")
        provider = kwargs.pop("backend")
    elif "oauth" in request.session:
        token = request.session["oauth"]
        provider = token["name"]
        kwargs.pop("token", None)
        kwargs.pop("backend", None)
    else:
        return None
    user = User(**kwargs)
    user.save()
    info = get_user_info(provider, token=token)
    token = OAuthToken(
        owner=user,
        provider=provider,
        identifier=info.identifier,
        access_token=token.get("access_token"),
        refresh_token=token.get("refresh_token"),
        expires_at=datetime.fromtimestamp(token.get("expires_at"))
    )
    token.save()
    user.backend = "multilogin.auth_backend.MultiloginBackend"
    return user
