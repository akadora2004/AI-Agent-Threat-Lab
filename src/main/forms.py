from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label="名前", max_length=150, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "password1", "password2")
        labels = {
            "username": "学籍番号",
            "first_name": "名前",
        }
