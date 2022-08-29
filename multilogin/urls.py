from django.urls import path, include
from .multilogin.main import create_urlpatterns, enabled_backends

app_name = "multilogin"

urlpatterns = []

for backend in enabled_backends():
    backend_urls = create_urlpatterns(backend)
    urlpatterns.append(path(f"{backend.NAME}/", include(backend_urls)))
