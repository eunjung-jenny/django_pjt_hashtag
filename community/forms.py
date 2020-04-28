from django import forms
from .models import Article, Comment, Hashtag

class ArticleForm(models.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']

class CommentForm(models.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class HaghtagForm(models.ModelForm):
    class Meta:
        model = Haghtag
        fields = ['tag']