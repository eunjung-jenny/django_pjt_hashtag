from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from .models import Article, Comment, Hashtag
from .forms import ArticleForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Count, Prefetch
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
import json

# Create your views here.


def index(request):
    articles = Article.objects.select_related('creator').prefetch_related(
        'like_users').annotate(like_users_count=Count('like_users')).order_by('-pk')
    term = None
    context = {
        'articles': articles,
        'term': term
    }
    return render(request, 'community/index.html', context)


@require_POST
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


@require_POST
@login_required
def like(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.user in article.like_users.all():
        article.like_users.remove(request.user)
        liked = False
    else:
        article.like_users.add(request.user)
        liked = True

    context = {
        'liked': liked,
        'count': article.like_users.count()
    }
    return JsonResponse(context)


@login_required
def detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    comment_form = CommentForm()
    child_comment_form = CommentForm()
    context = {
        'article': article,
        'comment_form': comment_form,
        'child_comment_form': child_comment_form,
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


@login_required
@require_POST
def comment_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.creator = request.user
        comment.article = article
        comment.save()
        messages.success(request, '댓글을 성공적으로 작성하였습니다.')
    else:
        messages.error(request, '댓글 작성에 실패하였습니다.')
    return redirect('community:detail', article_pk)


@login_required
@require_POST
def child_comment_create(request, article_pk, comment_pk):
    article = get_object_or_404(Article, pk=article_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        child_comment = form.save(commit=False)
        child_comment.creator = request.user
        child_comment.article = article
        child_comment.parent_comment = comment
        child_comment.save()
        messages.success(request, '대댓글을 성공적으로 작성하였습니다.')
    else:
        messages.error(request, '댓글 작성에 실패하였습니다.')
    return redirect('community:detail', article_pk)


@login_required
def comment_delete(request, article_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.creator:
        if not comment.child_comments.all():
            comment.delete()
            messages.success(request, '댓글을 삭제하였습니다.')
        else:
            messages.warning(request, '대댓글이 있는 댓글은 삭제할 수 없습니다.')
    else:
        messages.error(request, '댓글 삭제 권한이 없습니다.')
    return redirect('community:detail', article_pk)


@login_required
def child_comment_delete(request, article_pk, child_comment_pk):
    child_comment = get_object_or_404(Comment, pk=child_comment_pk)
    if request.user == child_comment.creator:
        child_comment.delete()
        messages.success(request, '댓글을 삭제하였습니다.')
    else:
        messages.error(request, '댓글 삭제 권한이 없습니다.')
    return redirect('community:detail', article_pk)
