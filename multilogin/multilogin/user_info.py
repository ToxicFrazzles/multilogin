class OAuthUserInfo(dict):
    REGISTERED_CLAIMS = [
        "identifier", "username", "preferred_username",
        "email", "email_verified", "picture"
    ]

    def __getattr__(self, key):
        try:
            return object.__getattribute__(self, key)
        except AttributeError as error:
            if key in self.REGISTERED_CLAIMS:
                return self.get(key)
            raise error
