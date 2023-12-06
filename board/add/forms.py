from django import forms

from .models import Post, UserResponse


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author',
            'title',
            'text',
            'category',
            'upload',
        ]


class ResponseForm(forms.ModelForm):
    class Meta:
        model = UserResponse
        fields = ['text']
