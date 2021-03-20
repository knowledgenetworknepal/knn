from django import forms
from .models import Comment, Quesiton
from ckeditor.fields import RichTextFormField

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control my-2'
            self.fields[field].widget.attrs['placeholder'] = 'Your comment here'


class DicussionForm(forms.ModelForm):
    class Meta:
        model = Quesiton
        fields = ('title','description','category')
        widgets = {
             'fields': RichTextFormField(),
          }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control my-2'
