from django import forms
from .models import Article, Comment, Hashtag

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        max_length=100,
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Minigram은 건전한 댓글 문화를 지향합니다.'
            })
    )

    class Meta:
        model = Comment
        fields = ['content']