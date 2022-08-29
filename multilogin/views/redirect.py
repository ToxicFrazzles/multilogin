from django.views import View
from django.shortcuts import reverse, resolve_url, redirect
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponseRedirect
from django.conf import settings


class RedirectView(View):
    backend = None

    def get(self, request):
        next_page = request.session.get("next", "/")
        request.session["next"] = None
        token = self.backend.authorize_access_token(request)
        resp = self.backend.get("users/@me", token=token)
        resp.raise_for_status()
        resp_json = resp.json()
        discord_user_id = resp_json.get("id", None)
        if not discord_user_id:
            return redirect(next_page or "/")
        user = authenticate(discord_user_id=discord_user_id)
        if user:
            login(request, user)
            return redirect(next_page)
        request.session['oauth'] = token
        request.session['oauth']["name"] = self.backend.name
        return HttpResponseRedirect(resolve_url(getattr(settings, "REGISTRATION_PAGE", "/")) + f"?next={next_page}")
