from django import forms
from django.core.exceptions import ValidationError

from .models import Tweet

MAX_LENGTH = 240


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) > MAX_LENGTH:
            raise ValidationError("This tweet is too long")
        return content
