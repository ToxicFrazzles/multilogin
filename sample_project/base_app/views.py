from django.shortcuts import render
from django.views import View

from multilogin.multilogin.main import get_user_info


class IndexView(View):
    def get(self, request):
        info = get_user_info("discord", request=request)
        return render(request, "base_app/index.html", context={'info': info})
