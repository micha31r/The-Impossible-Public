from django.forms import ModelForm, TextInput, PasswordInput
from django import forms

from .models import Feedback, Question

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = [
            "description"
        ]
        widgets = {
            "description":forms.Textarea(
                attrs={
                    "placeholder":"Write here"
                }
            ),
        }  


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            "short_description",
            "description"
        ]
        widgets = {
            "short_description":forms.TextInput(
                attrs={
                    "placeholder":"Brief overview"
                }
            ),
            "description":forms.Textarea(
                attrs={
                    "placeholder":"Details"
                }
            ),
        }  
