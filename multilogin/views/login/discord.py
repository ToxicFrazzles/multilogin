from django.views import View
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render, reverse, resolve_url
from django.contrib.auth import authenticate, login, get_user_model
from django.conf import settings
from ...models.discord_login import DiscordLogin

from ...authlib_configs import oauth

discord = oauth.create_client("discord")
User = get_user_model()


class DiscordLoginView(View):
    def get(self, request):
        redirect_uri = request.build_absolute_uri(reverse("multilogin:discord_redirect"))
        request.session["next"] = request.GET.get("next", None)
        return discord.authorize_redirect(
            request, redirect_uri
        )


class DiscordRedirectView(View):
    def get(self, request):
        next_page = request.session.get("next", None)
        request.session["next"] = None
        token = discord.authorize_access_token(request)
        resp = discord.get("users/@me", token=token)
        resp.raise_for_status()
        resp_json = resp.json()
        discord_user_id = resp_json.get("id", None)
        if not discord_user_id:
            return redirect(next_page or "/")
        user = authenticate(discord_user_id=discord_user_id)
        if user:
            login(request, user)
            return redirect(next_page or "/")
        request.session['oauth'] = {
            'model': DiscordLogin,
            'user_id': discord_user_id,
            'access_token': token["access_token"],
            'refresh_token': token["refresh_token"],
            'expires': token["expires_at"]
        }
        return HttpResponseRedirect(resolve_url(getattr(settings, "REGISTRATION_PAGE", "/")) + f"?next={next_page}")
