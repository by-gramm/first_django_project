from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class User(AbstractUser):
    RELATION_CHOICES = (
        (0, '가족 혹은 친척'),
        (1, '친구'),
        (2, '지인'),
        (3, '누군지 모르는')
    )

    # TODO: 이미지 파일 업로드 안 되는 문제 해결하기!
    profile_image = ProcessedImageField(
        upload_to='profile_image\%Y\%m\%d',
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 80},
    )
    relation_with_minki = models.SmallIntegerField(choices=RELATION_CHOICES, blank=False)
