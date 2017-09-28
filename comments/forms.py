from django import forms
from .models import Comments


class CommentsForms(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['name', 'email', 'url', 'text']
