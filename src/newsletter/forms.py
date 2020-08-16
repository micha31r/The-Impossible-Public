from django.forms import ModelForm, TextInput, PasswordInput
from django import forms

from .models import Subscriber

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = [
        	"email",
            "frequency",
        ]
        labels = {
            "email":"Email",
            "frequency":"Newsletter Frequency",
        }
       	widgets = {
            "email": forms.TextInput(attrs={'placeholder': 'Email address'}),
            "frequency":forms.RadioSelect(),
        }