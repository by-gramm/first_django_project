from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from .forms import SignupForm


# TODO: 회원가입과 동시에 로그인 되도록 구현
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "회원가입에 성공하셨습니다! 이민기 씨도 기뻐하시겠군요.")
            # TODO: 회원가입 후 리다이렉트 페이지 설정하기
            return redirect("/")
    else:
        form = SignupForm()
    return render(request, 'accounts/signup_form.html', {
        'form': form,
    })


login = LoginView.as_view(template_name='accounts/login_form.html')


logout = LogoutView.as_view()
