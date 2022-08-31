from django.contrib.auth import get_user_model, login
from django.shortcuts import render, redirect
from django.views import View

from multilogin.multilogin import get_user_info, register_user

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
        user = register_user(request, username=username, email=email)
        if not user:
            return redirect("register")
        login(request, user)
        return redirect("/")
