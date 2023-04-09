from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse
from django.views import View

from multilogin.multilogin import get_user_info, register_user, enabled_backends

User = get_user_model()


class IndexView(View):
    def get(self, request):
        try:
            info = get_user_info("discord", request=request)
        except:
            info = None

        logins = [
            (
                reverse(f"multilogin:{backend.NAME}"),
                backend.NAME,
                backend.NAME.capitalize()
            ) for backend in enabled_backends()
        ]
        return render(request, "base_app/index.html", context={'info': info, "logins": logins})


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
        user = register_user(request, username=username, email=email)
        if not user:
            return redirect("register")
        login(request, user)
        return redirect("/")


class LogOutView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("/")
        logout(request)
        return redirect("/")


class LoginRequiredView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "base_app/login_required.html")
