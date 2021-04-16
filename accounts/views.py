from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from .forms import SignupForm, ProfileForm


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            new_user = form.save()
            messages.success(request, "회원가입에 성공하셨습니다! 이민기 씨도 기뻐하시겠군요.")
            auth_login(request, new_user)
            return redirect('/')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup_form.html', {
        'form': form,
    })


# TODO: 비밀번호 입력받을 때 비밀번호가 안 보이게 하기
@login_required
def delete(request):
    if request.method == 'POST':
        user = request.user
        input_pwd = request.POST['input_pwd']
        if check_password(input_pwd, user.password):
            user.delete()
            messages.success(request, "회원 탈퇴가 완료되었습니다.")
            return redirect('/')
        else:
            messages.success(request, "비밀번호가 일치하지 않습니다.")
            return redirect('accounts:delete')
    return render(request, 'accounts/delete_form.html')


login = LoginView.as_view(template_name='accounts/login_form.html')


logout = LogoutView.as_view()


@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "프로필이 수정되었습니다.")
            return redirect('accounts:profile_edit')
    else:
        # 빈 폼을 할당할 경우, 사용자가 모든 정보를 처음부터 다시 입력해야 한다.
        # 따라서 instance=request.user를 인자로 주어, 사용자가 현재 정보에서 필요한 부분만 수정할 수 있게 한다.
        form = ProfileForm(instance=request.user)
    return render(request, "accounts/profile_edit_form.html", {
        'form': form,
    })


@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "비밀번호가 변경되었습니다.")
            return redirect('accounts:password_change')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "accounts/password_change_form.html", {
        'form': form,
    })
