from django.views import View
from django.shortcuts import redirect, render, reverse
from django.contrib.auth import authenticate, login, get_user_model
from django.utils import timezone
from ...models.discord_login import DiscordLogin

from ...authlib_configs import oauth

discord = oauth.create_client("discord")
User = get_user_model()


class DiscordLoginView(View):
    def get(self, request):
        redirect_uri = request.build_absolute_uri(reverse("multilogin:discord_redirect"))
        if "register" in request.GET:
            request.session["register"] = True
        return discord.authorize_redirect(
            request, redirect_uri
        )


class DiscordRedirectView(View):
    def get(self, request):
        register = request.session.get("register", False)
        request.session["register"] = False
        token = discord.authorize_access_token(request)
        print(token)
        resp = discord.get("users/@me", token=token)
        resp.raise_for_status()
        resp_json = resp.json()
        discord_user_id = resp_json.get("id", None)
        if not discord_user_id:
            return redirect("/")
        user = authenticate(discord_user_id=discord_user_id)
        if user:
            login(request, user)
            return redirect("/")
        if register:
            user = User(username=request.session.get("desired_username", None) or resp_json['username'])
            user.save()
            discord_login = DiscordLogin(
                user=user,
                discord_id=discord_user_id,
                access_token=token["access_token"],
                refresh_token=token["refresh_token"],
                expires=timezone.datetime.fromtimestamp(token["expires_at"])
            )
            discord_login.save()
            user = authenticate(discord_user_id=discord_user_id)
            print(user)
            print(user.backend)
            login(request, authenticate(discord_user_id=discord_user_id))
            return redirect("/")
        return redirect("/")

