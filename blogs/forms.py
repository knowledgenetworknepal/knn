from django import forms
from .models import Comment, Blog


class BaseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control my-2'
            self.fields[field].widget.attrs['placeholder'] = 'Your comment here'


class Blogform(BaseForm):
    class Meta:
        model = Blog
        fields = (
            'title',
            'author',
            'description',
            'category',
            'featured_image',
        )

        