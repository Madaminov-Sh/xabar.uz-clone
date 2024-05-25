from django import forms

from news.models import Comment
from common.models import Contact


class ContactModelForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)