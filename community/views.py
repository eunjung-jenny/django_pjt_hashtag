from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Comment, Hashtag
from .forms import ArticleForm, CommentForm, HaghtagForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles
    }
    return render(request, 'community/index.html', context)

@login_required
def post(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.creator = request.user
            article.save()
            messages.success(request, '글을 성공적으로 게시하였습니다.')
            return redirect('community:index')
        else:
            messages.error(request, '글 작성에 실패하였습니다.')
    else:
        form = ArticleForm()
    context = {
        'form': form
    }    
    return render(request, 'community/post.html', context)