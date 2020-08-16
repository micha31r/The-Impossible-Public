from django import forms
from .models import (
    Tag,
    Idea,
    Comment
)

DELETE_CHOICE = (
    (1, "Keep"),
    (2, "Delete"),
)

class IdeaForm(forms.ModelForm):
    delete = forms.IntegerField(label="",required=False,initial=1,widget=forms.Select(choices=DELETE_CHOICE))
    tags_remain = forms.CharField(label="Exsisting Tags",required=False)

    class Meta:
        model = Idea
        # Don't use "__all__", in this case the form won't validate
        fields = [
            "name",
            "short_description",
            "full_description",
            "tags",
            "publish_status",
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Title (Max 80)'}),
            'short_description': forms.Textarea(attrs={'placeholder': 'Description (Max 150)'}),
            'full_description': forms.Textarea(attrs={'placeholder': 'Content (Max 1000), use @username to mention other users'}),
        }
        labels={
            "name":"",
            "short_description":"",
            "full_description":"",
            "tags":"Tags",
            "publish_status":"Publish Status",
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # Don't use "__all__", in this case the form won't validate
        fields = [
            "full_description",
        ]
        widgets = {
            'full_description': forms.Textarea(attrs={'placeholder': 'Content (Max 500), use @username to mention other users'}),
        }
        labels={
            "full_description":"",
        }
