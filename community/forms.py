from django import forms
from .models import Article, Comment, Hashtag

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class HaghtagForm(forms.ModelForm):
    class Meta:
        model = Hashtag
        fields = ['tag']