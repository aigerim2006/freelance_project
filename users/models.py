from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    age = models.IntegerField(null=True, blank=True)
    user = models.OneToOneField(
        "auth.User", on_delete=models.CASCADE, related_name="profile"
    )
    photo = models.ImageField(upload_to="users/", blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    