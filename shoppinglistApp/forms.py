from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailOnlySignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data["email"].lower()
        user.username = email
        user.email = email
        if commit:
            user.save()
        return user


class NoOpPasswordResetForm(PasswordResetForm):
    def save(self, *args, **kwargs):
        # Prevent Django’s default email send
        pass