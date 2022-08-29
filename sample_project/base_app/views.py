from django.contrib.auth import get_user_model, login, authenticate
from django.shortcuts import render, redirect
from django.views import View
from django.utils.timezone import datetime

from multilogin.multilogin import get_user_info
from multilogin.models import OAuthToken

User = get_user_model()


class IndexView(View):
    def get(self, request):
        info = get_user_info("discord", request=request)
        return render(request, "base_app/index.html", context={'info': info})


class RegistrationView(View):
    def get(self, request):
        if "oauth" not in request.session:
            return redirect("/")
        ctx = {
            'info': get_user_info(
                request.session["oauth"]["name"],
                token=request.session["oauth"]
            )
        }
        return render(request, "base_app/register.html", context=ctx)

    def post(self, request):
        username = request.POST.get("username")
        email = request.POST.get("email")
        user = User(username=username, email=email)
        user.save()
        session_token = request.session["oauth"]
        info = get_user_info(session_token.get("name"), token=session_token)
        token = OAuthToken(
            owner=user,
            provider=session_token.get("name"),
            identifier=info.identifier,
            access_token=session_token.get("access_token"),
            refresh_token=session_token.get("refresh_token"),
            expires_at=datetime.fromtimestamp(session_token.get("expires_at"))
        )
        token.save()
        user = authenticate(
            auth_provider=session_token.get("name"),
            identifier=info.identifier
        )
        print(user)
        login(request, user)
        return redirect("/")
