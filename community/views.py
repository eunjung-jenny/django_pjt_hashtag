from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from .models import Article, Comment, Hashtag
from .forms import ArticleForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

BASE_URL = 'http://127.0.0.1:8000'

# Create your views here.
def index(request):
    articles = Article.objects.all()
    term = None
    context = {
        'articles': articles,
        'term': term
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
                if not Hashtag.objects.filter(tag=hashtag).exists():
                    h = Hashtag()
                    h.tag = hashtag.strip()
                    h.save()
                else:
                    h = Hashtag.objects.get(tag=hashtag)
                
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
    if request.META.get('HTTP_REFERER'):
        previous_url = request.META.get('HTTP_REFERER')

        # 로그인 페이지에서 넘어오는 경우, 좋아요 카운팅 하지 않고 디테일 페이지 보여줌
        if previous_url != BASE_URL + resolve_url('community:index') and previous_url != BASE_URL + resolve_url('community:detail', article_pk):
            return redirect('community:detail', article_pk)

        if request.user in article.like_users.all():
            article.like_users.remove(request.user)
            messages.warning(request, '좋아요를 취소하였습니다.')    
        else:
            article.like_users.add(request.user)
            messages.success(request, '좋아요를 눌렀습니다.')
        
        if previous_url == BASE_URL + resolve_url('community:index'):
            return redirect('community:index')
        elif previous_url == BASE_URL + resolve_url('community:detail', article_pk):
            return redirect('community:detail', article_pk)            

    # 외부 페이지에서 넘어오는 경우
    else:
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
        'articles': articles,
        'term': term,
    }
    return render(request, 'community/index.html', context)