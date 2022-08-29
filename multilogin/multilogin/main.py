from django.conf import settings
from django.urls import path
from authlib.integrations.django_client import OAuth
from multilogin.models import OAuthToken
from ..views import LoginView, RedirectView
from . import backends


available_backends = [
    backends.Discord
]


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


def create_urlpatterns(backend):
    if isinstance(backend, str):
        backend = getattr(backends, backend)
    backend.OAUTH_CONFIG.update(
        client_id=getattr(settings, f"{backend.NAME.upper()}_CLIENT_ID", None),
        client_secret=getattr(settings, f"{backend.NAME.upper()}_CLIENT_SECRET", None)
    )
    third_party = oauth.register(
        backend.NAME,
        False,
        **backend.OAUTH_CONFIG
    )
    return [
        path('', LoginView.as_view(backend=third_party), name=f'{backend.NAME}_login'),
        path('redirect/', RedirectView.as_view(backend=third_party), name=f'{backend.NAME}_redirect'),
    ]


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
