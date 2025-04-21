from django.db import models
from django.conf import settings
from google.oauth2.credentials import Credentials


class YouTubeCredential(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=2
    )
    token = models.TextField()
    refresh_token = models.TextField()
    token_uri = models.TextField()
    client_id = models.TextField()
    client_secret = models.TextField()
    scopes = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    @classmethod
    def save_credentials(cls, user, credentials):
        # Get or create the credential object
        cred_obj, created = cls.objects.get_or_create(user=user)

        # Encrypt sensitive fields
        cred_obj.token = credentials.token
        cred_obj.refresh_token = credentials.refresh_token
        cred_obj.token_uri = credentials.token_uri
        cred_obj.client_id = credentials.client_id
        cred_obj.client_secret = credentials.client_secret
        cred_obj.scopes = ",".join(credentials.scopes)
        cred_obj.save()
        return cred_obj

    def get_credentials(self):
        """Get Google OAuth credentials object from saved data"""
        return Credentials(
            token=self.token,
            refresh_token=self.refresh_token,
            token_uri=self.token_uri,
            client_id=self.client_id,
            client_secret=self.client_secret,
            scopes=self.scopes.split(","),
        )
