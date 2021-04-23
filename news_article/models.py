from django.db import models
from django.conf import settings


class Article(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False)
    article_image = models.ImageField(blank=True, upload_to='article_image/%Y/%m/%d')
    content = models.TextField(max_length=2000, blank=False, help_text="2,000자 이내로 작성해 주세요.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']
