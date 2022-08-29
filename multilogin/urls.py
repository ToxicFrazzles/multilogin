from django.urls import path, include
from .multilogin.main import enabled_backends, oauth
from .multilogin.urls import create_urlpatterns

app_name = "multilogin"

urlpatterns = []

for backend in enabled_backends():
    backend_urls = create_urlpatterns(backend, oauth)
    urlpatterns.append(path(f"{backend.NAME}/", include(backend_urls)))
