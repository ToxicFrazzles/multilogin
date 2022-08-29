from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class OAuthToken(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    provider = models.CharField(max_length=32, db_index=True)
    identifier = models.CharField(max_length=128, db_index=True)
    access_token = models.TextField()
    refresh_token = models.TextField()
    expires_at = models.DateTimeField()

