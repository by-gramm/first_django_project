from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from happy_birthday.forms import PostForm


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
            return redirect('happy_birthday')
    else:
        form = PostForm()
    return render(request, "happy_birthday/post_form.html", {
        'form': form,
    })
