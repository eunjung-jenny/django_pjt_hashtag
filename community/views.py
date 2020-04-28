from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Comment, Hashtag
from .forms import ArticleForm, CommentForm
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
            
            hashtags = request.POST['hashtags'].split('#')[1:]
            for hashtag in hashtags:
                h = Hashtag()
                h.tag = hashtag.strip()
                h.save()
            
                h.has_articles.add(article)
                
            messages.success(request, '글을 성공적으로 게시하였습니다.')
            return redirect('community:index')
        else:
            messages.error(request, '글 작성에 실패하였습니다.')
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }    
    return render(request, 'community/form.html', context)

@login_required
def like(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.user in article.like_users.all():
        article.like_users.remove(request.user)    
    else:
        article.like_users.add(request.user)
    return redirect('community:detail', article_pk)

@login_required
def detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    context = {
        'article': article,
    }
    return render(request, 'community/detail.html', context)

@login_required
def edit(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.user == article.creator:
        if request.method == 'POST':
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                for hashtag in article.has_hashtags.all():
                    hashtag.delete()

                article = form.save(commit=False)
                article.creator = request.user
                article.save()

                hashtags = request.POST['hashtags'].split('#')[1:]
                for hashtag in hashtags:
                    if not Hashtag.objects.filter(tag=hashtag).exists():
                        h = Hashtag()
                        h.tag = hashtag.strip()
                        h.save()
                    else:
                        h = Hashtag.objects.get(tag=hashtag)
                    
                    h.has_articles.add(article)
                messages.success(request, '글을 성공적으로 수정하였습니다.')
                return redirect('community:detail', article_pk) 
            else:
                messages.error(request, '글 수정에 실패하였습니다.')
        else:
            form = ArticleForm(instance=article)
            hashtags = ''
            for hashtag in article.has_hashtags.all():
                hashtags += f'#{hashtag.tag}'
        context = {
            'form': form,
            'hashtags': hashtags
        }    
        return render(request, 'community/form.html', context)
    else:
        messages.error(request, '수정 권한이 없습니다.')   
        return redirect('community:detail', article_pk)

def delete(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'POST' and request.user.is_authenticated and request.user == article.creator:
        article.delete()
    return redirect('community:index')

def search(request):
    term = request.GET.get('term')
    is_exist = Hashtag.objects.filter(tag=term).exists()        
    if is_exist:
        hashtag = Hashtag.objects.get(tag=term)
        articles = Article.objects.filter(has_hashtags=hashtag)
    else:
        articles = []
    context = {
        'articles': articles
    }
    return render(request, 'community/index.html', context)