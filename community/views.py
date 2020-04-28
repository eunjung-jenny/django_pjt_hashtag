from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Comment, Hashtag
from .forms import ArticleForm, CommentForm, HashtagForm
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
        article_form = ArticleForm(request.POST)
        hashtag_form = HashtagForm(request.POST)
        if article_form.is_valid() and hashtag_form.is_valid():
            article = article_form.save(commit=False)
            article.creator = request.user
            article.save()
            
            hashtags = request.POST['tag'].split('#')[1:]
            for hashtag in hashtags:
                h = Hashtag()
                h.tag = hashtag
                h.save()
            
                h.has_articles.add(article)
                
            messages.success(request, '글을 성공적으로 게시하였습니다.')
            return redirect('community:index')
        else:
            messages.error(request, '글 작성에 실패하였습니다.')
    else:
        article_form = ArticleForm()
        hashtag_form = HashtagForm()
    context = {
        'article_form': article_form,
        'hashtag_form': hashtag_form
    }    
    return render(request, 'community/post.html', context)

@login_required
def like(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.user in article.like_users.all():
        article.like_users.remove(request.user)    
    else:
        article.like_users.add(request.user)
    return redirect('community:index')

@login_required
def detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    context = {
        'article': article,
    }
    return render(request, 'community/detail.html', context)