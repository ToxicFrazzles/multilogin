from django.views import View
from django.shortcuts import reverse, resolve_url, redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.http.response import HttpResponseRedirect
from django.conf import settings
from django.utils.timezone import datetime
from ..multilogin.main import get_user_info
from ..models import OAuthToken


class RedirectView(View):
    backend = None

    def get(self, request):
        next_page = request.session.get("next", "/")
        request.session.pop("next", None)
        token = self.backend.authorize_access_token(request)
        userinfo = get_user_info(self.backend.name, token=token)
        if not userinfo.identifier:
            return redirect(next_page)
        if request.user.is_authenticated:
            db_token = OAuthToken(
                owner=request.user,
                provider=self.backend.name,
                identifier=userinfo.identifier,
                access_token=token.get("access_token", None),
                refresh_token=token.get("refresh_token"),
                expires_at=datetime.fromtimestamp(token.get("expires_at"))
            )
            db_token.save()
            request.user.set_unusable_password()
            request.user.save()
            update_session_auth_hash(request, request.user)
            return redirect(next_page)
        user = authenticate(
            auth_provider=self.backend.name,
            identifier=userinfo.identifier
        )
        if user:
            login(request, user)
            return redirect(next_page)
        request.session['oauth'] = token
        request.session['oauth']["name"] = self.backend.name
        return HttpResponseRedirect(resolve_url(getattr(settings, "REGISTRATION_PAGE", "/")) + f"?next={next_page}")
