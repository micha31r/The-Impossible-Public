from django.forms import ModelForm, TextInput, PasswordInput
from django import forms

from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder":"Username"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder":"Password"
            }
        )
    )

class SignUpForm(forms.Form):
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "placeholder":"First Name"
            }
        )
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "placeholder":"Last Name"
            }
        )
    )
    username = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "placeholder":"Username"
            }
        )
    )
    email = forms.EmailField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "placeholder":"Email"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder":"Password"
            }
        )
    )
    password_confirmation = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder":"Confirm Password"
            }
        )
    )

class VerificationForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        widget=forms.TextInput(
            attrs={
                "placeholder":"Code"
            }
        )
    )

# Below are all account setting related

class ProfileForm(forms.Form):
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "placeholder":"First Name"
            }
        )
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "placeholder":"Last Name"
            }
        )
    )
    email = forms.EmailField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "placeholder":"Email"
            }
        )
    )
    bio = forms.CharField(
        max_length=160,
        widget=forms.Textarea(
            attrs={
                "placeholder":"Bio (160)"
            }
        ),
        required=False
    )
    website = forms.URLField(
        max_length=160,
        widget=forms.TextInput(
            attrs={
                "placeholder":"Website"
            }
        ),
        required=False
    )
    location = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "placeholder":"Location (Planet Earth?)"
            }
        ),
        required=False
    )

class PasswordForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder":"Current Password"
            }
        ),
        required=False
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder":"New Password"
            }
        ),
        required=False
    )
    password_confirmation = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder":"Confirm Password"
            }
        ),
        required=False
    )

class ExploreContentForm(forms.ModelForm):
    tags_remain = forms.CharField(label="Tags Remain",required=False)

    class Meta:
        model = Profile
        fields = [
            "tags",
        ]
        labels={
            "tags":"Tags",
        }

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "like_setting",
            "comment_setting",
        ]
        labels={
            "like_setting":"Likes",
            "comment_setting":"Comments",
        }
        widgets = {
            "like_setting":forms.RadioSelect(),
            "comment_setting":forms.RadioSelect(),
        }  

class PrivacyForm(forms.ModelForm):
    blocked_user = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder":"Type @username to block"
            }
        ),
        required=False
    )

    class Meta:
        model = Profile
        fields = [
            "discover_setting",
        ]
        labels={
            "discover_setting":"Discover",
        }
        widgets = {
            "discover_setting":forms.RadioSelect(),
        } 

class SearchForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder":"@"
            }
        )
    )