from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SignupForm


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "회원가입에 성공하셨습니다! 이민기 씨도 기뻐하시겠군요.")
            return redirect("/")
    else:
        form = SignupForm()
    return render(request, 'accounts/signup_form.html', {
        'form': form,
    })
