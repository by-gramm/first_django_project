from django.contrib import admin
from happy_birthday.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass
