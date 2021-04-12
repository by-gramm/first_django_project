from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # TODO: 선택할 수 있게 하기
    relation_with_minki = models.CharField(max_length=100)
