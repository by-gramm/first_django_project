from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['profile_image', 'username', 'email', 'relation_with_minki']

        def clean_email(self):
            email = self.cleaned_data.get('email')

            if email and User.objects.filter(email=email).exists():
                raise forms.ValidationError('어이쿠, 이미 등록된 이메일이네요.')
            return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_image', 'username', 'email', 'relation_with_minki']
