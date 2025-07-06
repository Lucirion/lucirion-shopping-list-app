from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User

class EmailOnlySignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]  # use email as username internally
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class NoOpPasswordResetForm(PasswordResetForm):
    def save(self, *args, **kwargs):
        # Override default behavior to stop Django from sending its own password reset email
        pass
