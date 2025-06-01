from django import forms
from .models import Post, Comment


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'is_published', 'categories','tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'post title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'post content'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'comment content', 'rows': 4}),
        }

class PostSearchForm(forms.Form):
    q = forms.CharField(label='Search', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
