from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from happy_birthday.forms import PostForm, CommentForm
from happy_birthday.models import Post, Comment


@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # 필수 필드에 대한 값 지정 없이 바로 save()를 호출하면 IntegrityError 발생
            # 따라서 save(commit=False)로 데이터베이스 저장을 미루고,
            # 필수 필드 저장 후 다시 save()를 호출하여 데이터베이스에 저장한다.
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, f"{request.user}님의 편지가 전송되었습니다.")
            return redirect('happy_birthday:index')
    else:
        form = PostForm()
    return render(request, "happy_birthday/post_form.html", {
        'form': form,
    })


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    comment_form = CommentForm()
    return render(request, "happy_birthday/post_detail_form.html", {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    })


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.warning(request, "떽! 남의 편지에 손 대면 안 돼요!")
        return redirect('happy_birthday:post_detail', pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, f"{request.user}님의 편지가 다시 전송되었습니다.")
            return redirect('happy_birthday:index')
    else:
        form = PostForm(instance=post)
    return render(request, "happy_birthday/post_form.html", {
        'form': form,
    })


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.warning(request, "떽! 남의 편지를 삭제하려고 하다니!")
        return redirect('happy_birthday:post_detail', pk=pk)

    post.delete()
    messages.success(request, f"{request.user}님의 편지는 이제 눈을 씻고 찾아봐도 찾을 수 없습니다!")
    return redirect('happy_birthday:index')


def index(request):
    post_list = Post.objects.all()
    return render(request, "happy_birthday/index.html", {
        'post_list': post_list,
    })


@login_required
def comment_new(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('happy_birthday:post_detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, "comment_form.html", {
        'form': form,
    })


@login_required
def comment_delete(request, pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    if comment.author != request.user:
        messages.warning(request, "떽! 남의 댓글에 손 대면 안 돼요!")
        return redirect('happy_birthday:post_detail', pk=pk)

    comment.delete()
    messages.success(request, f"{request.user}님의 댓글은 이제 눈을 씻고 찾아봐도 찾을 수 없습니다!")
    return redirect('happy_birthday:post_detail', pk=pk)
