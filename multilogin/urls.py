from django.urls import path, include
from .views.login import urls as login_urls


app_name = "multilogin"

urlpatterns = [
    path("login/", include(login_urls)),
]
