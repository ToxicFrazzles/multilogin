from ..models.discord_login import DiscordLogin


def fetch_discord_token(request):
    token = DiscordLogin.objects.get(user=request.user)
    return token.to_token()


class Discord:
    NAME = "discord"
    OAUTH_CONFIG = {
        "api_base_url": "https://discord.com/api/",
        "access_token_url": "https://discord.com/api/oauth2/token",
        "authorize_url": "https://discord.com/api/oauth2/authorize",
        "client_kwargs": {
            "token_endpoint_auth_method": "client_secret_post",
            "scope": "identify",
            "grant_type": "authorization_code"
        },
        "fetch_token": fetch_discord_token
    }
