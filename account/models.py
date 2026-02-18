from django.contrib.auth.models import AbstractUser, User
from django.db import models


class UserExt(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    uid = models.CharField(max_length=255, unique=True, verbose_name='UID')
    rid = models.CharField(max_length=15, unique=True, verbose_name='RID')

    def __str__(self):
        return f"{self.user.username}'s profile"