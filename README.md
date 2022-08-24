# Multilogin
Django app that provides Oauth2 based login


## Usage
This can be used in a Django project as well as or instead of the default authentication backend.
To do this several settings need to be setup in your project.

1. The app needs to be installed.
    * `pip install git+https://github.com/ToxicFrazzles/multilogin.git#egg=multilogin`
2. The app needs to be included in the `INSTALLED_APPS` setting
3. The required authentication backends need to be added to the `AUTHENTICATION_BACKENDS` setting
    * Discord: `multilogin.auth_backends.discord.DiscordLoginBackend`
4. The client IDs and secrets for each backend must be specified in the settings e.g.
    * `DISCORD_CLIENT_ID = "123456789123456789"`
    * `DISCORD_CLIENT_SECRET = "QwErTyUiOpAsDfGhJkLzXcVbNmQwErTy"`
5. The urls for multilogin need to be included in the root urls config
   * ```python
     from django.contrib import admin
     from django.urls import path, include
     import multilogin.urls
     
     urlpatterns = [
         path('auth/', include(multilogin.urls)),
         path('admin/', admin.site.urls),
     ]
     ```
6. Migrations need to be applied
   * `python manage.py migrate`

And that should cover it. 
Provided the settings have been set up correctly the login URL for a provider should be available through "multilogin:***Provider_name***" in the `reverse()` function or in the url template tag e.g.
`reverse("multilogin:discord")` or `{% url 'multilogin:discord' %}`

## Supported OAuth2 Providers
* Discord

Pull requests to add others are welcomed.
