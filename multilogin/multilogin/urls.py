from django.conf import settings
from django.urls import path
from . import backends
from ..views import LoginView, RedirectView


def create_urlpatterns(backend, oauth):
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
        path('', LoginView.as_view(backend=third_party), name=f'{backend.NAME}'),
        path('redirect/', RedirectView.as_view(backend=third_party), name=f'{backend.NAME}_redirect'),
    ]