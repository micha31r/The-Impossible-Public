from django import forms
from .models import File
 
class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = [
            "description",
            "file",
        ]
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'Description (Max 120)'})
        }
        labels={
            "description":"",
            "file":""
        }
