from django.db import models

class FacebookToken(models.Model):
    user_id = models.CharField(max_length=100)
    access_token = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_id
