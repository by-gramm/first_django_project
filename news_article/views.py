from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from news_article.forms import ArticleForm
from news_article.models import Article


@login_required
def article_new(request):
    user = request.user
    if not user.is_staff:
        messages.error(request, "스태프 유저만 기사를 작성할 수 있습니다.")
        return redirect('/')

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = user
            post.save()
            messages.success(request, f"{request.user}님의 기사가 업로드되었습니다.")
            return redirect('/')
    else:
        form = ArticleForm()
    return render(request, "news_article/article_form.html", {
        'form': form,
    })


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, "news_article/article_detail_form.html", {
        'article': article,
    })


@login_required
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if article.author != request.user:
        messages.warning(request, "떽! 남의 기사에 손 대면 안 돼요!")
        return redirect('article:article_detail', pk=pk)

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, f"{request.user}님의 기사가 수정되었습니다.")
            return redirect('article:article_detail', pk=pk)
    else:
        form = ArticleForm(instance=article)
    return render(request, "news_article/article_form.html", {
        'form': form,
    })


@login_required
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if article.author != request.user:
        messages.warning(request, "떽! 남의 기사를 삭제하려고 하다니!")
        return redirect('article:article_detail', pk=pk)

    article.delete()
    messages.success(request, f"{request.user}님의 기사가 정상적으로 삭제되었습니다.")
    return redirect('/')
