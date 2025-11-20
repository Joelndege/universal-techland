from django import forms
from .models import ForumPost, Comment

class ForumPostForm(forms.ModelForm):
    """
    Form for creating and editing forum posts.
    """
    class Meta:
        model = ForumPost
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title...',
                'maxlength': 200
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Share your thoughts, experiences, or questions...',
                'rows': 6
            })
        }
        labels = {
            'title': 'Post Title',
            'content': 'Post Content'
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title.strip()) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content.strip()) < 10:
            raise forms.ValidationError("Content must be at least 10 characters long.")
        return content


class CommentForm(forms.ModelForm):
    """
    Form for adding comments to forum posts.
    """
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Add your comment...',
                'rows': 3
            })
        }
        labels = {
            'content': 'Your Comment'
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content.strip()) < 1:
            raise forms.ValidationError("Comment cannot be empty.")
        return content
