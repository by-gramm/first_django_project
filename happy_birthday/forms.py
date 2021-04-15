from django import forms
from happy_birthday.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
