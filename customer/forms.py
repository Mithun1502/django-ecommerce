from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
import re


class RegisterForm(forms.Form):

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Username"}
        ),
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Enter email"}
        )
    )

    mobile = forms.CharField(
        max_length=10,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Mobile Number"}
        ),
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter Password"}
        )
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirm Password"}
        )
    )

    def clean_username(self):
        username = self.cleaned_data.get("username", "").strip()

        if not re.fullmatch(r"[A-Za-z_]+", username):
            raise forms.ValidationError(
                "Username can contain only letters and Underscores"
            )

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")

        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")

        return email

    def clean_mobile(self):
        mobile = self.cleaned_data.get("mobile")

        if not mobile.isdigit():
            raise forms.ValidationError("Mobile number must contain only digits")

        if len(mobile) != 10:
            raise forms.ValidationError("Mobile number must be exactly 10 digits")

        if UserProfile.objects.filter(mobile=mobile).exists():
            raise forms.ValidationError("Mobile number already exists")
        if not mobile.startswith(("6", "7", "8", "9")):
            raise forms.ValidationError("Mobile number must start with 6, 7, 8, or 9.")

        return mobile

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                self.add_error("confirm_password", "Passwords do not match")

        return cleaned_data


class LoginForm(forms.Form):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Username"}
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Enter Password"}
        )
    )


class CheckoutForm(forms.Form):
    # username = forms.CharField(
    #     max_length=150,
    #     widget=forms.TextInput(
    #         attrs={"class": "form-control", "placeholder": "Enter Username"}
    #     ),
    # )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Enter Email"}
        )
    )
    mobile = forms.CharField(
        max_length=10,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter Mobile"}
        ),
    )

    address = forms.CharField(
        max_length=266,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your address (Max 200 Characters)",
                "rows": 5,
            }
        ),
    )

    # def clean_username(self):
    #     username = self.cleaned_data.get("username", "").strip()

    #     if not re.fullmatch(r"[A-Za-z]+", username):
    #         raise forms.ValidationError("Username can contain only letters and spaces")

    #     return username

    def clean_email(self):
        email = self.cleaned_data.get("email")

        return email

    def clean_mobile(self):
        mobile = self.cleaned_data.get("mobile")
        if not mobile.isdigit():
            raise forms.ValidationError("Mobile number must contain only digits")

        if len(mobile) != 10:
            raise forms.ValidationError("Mobile number must be exactly 10 digits")

        if UserProfile.objects.filter(mobile=mobile).exists():
            raise forms.ValidationError("Mobile number already exists")

        if not mobile.startswith(("6", "7", "8", "9")):
            raise forms.ValidationError("Mobile number must start with 6, 7, 8, or 9.")

        return mobile


class EditProfileForm(forms.Form):

    username = forms.CharField(
        max_length=150, widget=forms.TextInput(attrs={"class": "form-control"})
    )

    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))

    mobile = forms.CharField(
        max_length=10, widget=forms.TextInput(attrs={"class": "form-control"})
    )

    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4}),
    )

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data["username"]

        if User.objects.exclude(id=self.user.id).filter(username=username).exists():
            raise forms.ValidationError("Username already exists")

        return username

    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.exclude(id=self.user.id).filter(email=email).exists():
            raise forms.ValidationError("Email already exists")

        return email

    def clean_mobile(self):
        mobile = self.cleaned_data["mobile"]

        if UserProfile.objects.exclude(user=self.user).filter(mobile=mobile).exists():
            raise forms.ValidationError("Mobile already exists")

        return mobile
