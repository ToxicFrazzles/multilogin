from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class OAuthToken(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    provider = models.CharField(max_length=32, db_index=True)
    identifier = models.CharField(max_length=128, db_index=True)
    access_token = models.TextField(null=True, default=None)
    refresh_token = models.TextField()
    expires_at = models.DateTimeField()

    class Meta:
        verbose_name = "OAuth Token"
        verbose_name_plural = "OAuth Tokens"

    def __str__(self):
        return f"{self.owner}: {self.provider}"

    def to_token(self):
        return {
            "name": self.provider,
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires_at": self.expires_at.timestamp()
        }

