from ..user_info import OAuthUserInfo


def normalise_userinfo(client, data):
    user_info = {
        "identifier": data.get("id", None),
        "username": data.get("username", None),
        "preferred_username": data.get("username", None),
        "email": data.get("email", None),
        "email_verified": data.get("email_verified", False)
    }
    if "avatar" in data:
        user_info['picture'] = f"https://cdn.discordapp.com/avatars/{data['id']}/{data['avatar']}.png"
    return OAuthUserInfo(user_info)


class Discord:
    NAME = "discord"
    OAUTH_CONFIG = {
        "api_base_url": "https://discord.com/api/",
        "access_token_url": "https://discord.com/api/oauth2/token",
        "authorize_url": "https://discord.com/api/oauth2/authorize",
        "client_kwargs": {
            "token_endpoint_auth_method": "client_secret_post",
            "scope": "identify+email",
            "grant_type": "authorization_code"
        },
        'userinfo_endpoint': 'https://discord.com/api/users/%40me',
        'userinfo_compliance_fix': normalise_userinfo
    }
