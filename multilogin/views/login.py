from django.views import View
from django.shortcuts import reverse


class LoginView(View):
    backend = None

    def get(self, request):
        redirect_uri = request.build_absolute_uri(reverse(f"multilogin:{self.backend.name}_redirect"))
        if "next" in request.GET:
            request.session["next"] = request.GET.get("next", "/")
        return self.backend.authorize_redirect(
            request, redirect_uri
        )
