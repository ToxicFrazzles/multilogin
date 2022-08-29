from django.views import View
from django.shortcuts import reverse, resolve_url, redirect
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponseRedirect
from django.conf import settings
from ..multilogin.main import get_user_info


class RedirectView(View):
    backend = None

    def get(self, request):
        next_page = request.session.get("next", "/")
        request.session["next"] = None
        token = self.backend.authorize_access_token(request)
        userinfo = get_user_info(self.backend.name, token=token)
        if not userinfo.identifier:
            return redirect(next_page or "/")
        user = authenticate(auth_provider=self.backend.name, identifier=f"userinfo.identifier")
        if user:
            login(request, user)
            return redirect(next_page)
        request.session['oauth'] = token
        request.session['oauth']["name"] = self.backend.name
        return HttpResponseRedirect(resolve_url(getattr(settings, "REGISTRATION_PAGE", "/")) + f"?next={next_page}")
