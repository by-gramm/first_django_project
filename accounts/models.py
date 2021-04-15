from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import resolve_url
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class User(AbstractUser):
    RELATION_CHOICES = (
        (0, '가족 혹은 친척'),
        (1, '친구'),
        (2, '지인'),
        (3, '누군지 모르는')
    )

    profile_image = ProcessedImageField(
        blank=True,
        upload_to='profile_image/%Y/%m/%d',
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 80},
    )
    relation_with_minki = models.SmallIntegerField(choices=RELATION_CHOICES, blank=False)


    @property
    def profile_image_url(self):
        if self.profile_image:
            return self.profile_image.url
        else:
            return "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"
