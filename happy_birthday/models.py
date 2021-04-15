from django.conf import settings
from django.db import models
from django.urls import reverse


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000, blank=False, help_text="1,000자 이내로 작성해 주세요.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # TODO: 댓글 클래스 만들고 연결하기

    def get_absolute_url(self):
        return reverse("happy_birthday:post_detail", args=[self.pk])

    class Meta:
        ordering = ['-id']
