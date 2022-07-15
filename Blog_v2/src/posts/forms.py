from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("__all__")

class CommentForm(forms.ModelForm):

    class Meta: 
        model = Comment
        fields = ('content', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""