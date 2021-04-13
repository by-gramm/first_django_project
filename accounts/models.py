from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    RELATION_CHOICES = (
        (0, '가족 혹은 친척'),
        (1, '친구'),
        (2, '지인'),
        (3, '누군지 모르는')
    )

    profile_image = models.ImageField(upload_to='profile_image\%Y\%m\%d', blank=True)
    relation_with_minki = models.SmallIntegerField(choices=RELATION_CHOICES, blank=False)

