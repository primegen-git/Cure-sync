from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from user.models import Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "username", "email", "password1", "password2"]
        labels = {
            "first_name": "Name",
            "username": "Username",
            "email": "Email",
            "password1": "Password",
            "password2": "Confirm Password",
        }

    usable_password = None


class ProfileCreationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ["user", "name"]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"placeholder": "YYYY-MM--DD"}),
        }
