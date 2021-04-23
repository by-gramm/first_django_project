from django.forms import forms
from news_article.models import Article


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'article_image', 'content']
