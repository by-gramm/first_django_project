import os
import requests
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.views import LoginView, LogoutView
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from .forms import SignupForm, ProfileForm
from .models import User


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


@login_required
def delete(request):
    if request.method == 'POST':
        user = request.user
        if user.login_method == 'kakao':
            user.delete()
            messages.success(request, "회원 탈퇴가 완료되었습니다.")
            return redirect('/')
        else:
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


def kakao_login(request):
    rest_api_key = str(os.getenv('KAKAO_ID'))
    redirect_uri = "https://minkitimes.herokuapp.com/accounts/login/kakao/callback/"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri={redirect_uri}&response_type=code"
    )


def kakao_callback(request):
    if request.user.is_authenticated:
        messages.error(request, "이미 로그인되어 있습니다.")
        return redirect('/')

    code = request.GET.get("code", None)
    if code is None:
        messages.error(request, "로그인에 실패했습니다.")
        return redirect('/')

    rest_api_key = str(os.getenv('KAKAO_ID'))
    redirect_uri = "https://minkitimes.herokuapp.com/accounts/login/kakao/callback/"
    client_secret = str(os.getenv('CLIENT_SECRET_KEY'))
    request_access_token = requests.post(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={rest_api_key}&redirect_uri={redirect_uri}&code={code}&client_secret={client_secret}",
        headers={"Accept": "application/json"},
    )
    access_token_json = request_access_token.json()

    error = access_token_json.get("error", None)
    if error is not None:
        print(error)
        messages.error("토큰에 접근할 수 없습니다.")
        return redirect('/')

    access_token = access_token_json.get("access_token")
    headers = {"Authorization": f"Bearer {access_token}"}
    profile_request = requests.post(
        "https://kapi.kakao.com/v2/user/me",
        headers=headers,
    )
    profile_json = profile_request.json()
    kakao_account = profile_json.get("kakao_account")
    profile = kakao_account.get("profile")

    username = profile.get("nickname", None)
    profile_image_url = profile.get("profile_image_url", None)
    email = kakao_account.get("email", None)

    # 카카오 유저 정보에서 가져온 이메일과 같은 이메일을 쓰는 유저가 있는 경우,
    # 그 유저가 카카오 가입 유저가 아니라면 에러 메세지를 보여주고,
    # 카카오 가입 유저라면 바로 로그인시킨다.
    user = User.objects.filter(email=email).first()
    if not user:
        # 카카오톡 사용자 이름이 이미 사용 중인 username과 겹치는 경우,
        # 겹치지 않도록 뒤에 숫자를 붙여준다.
        user = User.objects.filter(username=username).first()
        if user:
            username += '2'
            num_for_username = 2

            while True:
                user = User.objects.filter(username=username).first()
                if user:
                    username = username[:-1] + str(num_for_username)
                    num_for_username += 1
                else:
                    break

        user = User.objects.create_user(
            email=email,
            username=username,
            login_method='kakao',
        )

        if profile_image_url is not None:
            profile_image_request = requests.get(profile_image_url)
            user.profile_image.save(
                f"{username}의 프로필 사진", ContentFile(profile_image_request.content)
            )

    if user.login_method == 'email':
        messages.error(request, "해당 계정은 이미 가입되어 있습니다. 사용자 이름/비밀번호로 로그인해주세요.")
        return redirect('accounts:login')

    user.set_unusable_password()
    user.save()
    messages.success(request, "카카오로 로그인했습니다.")
    auth_login(request, user)
    return redirect('accounts:profile_edit')


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
    user = request.user
    if user.login_method == 'kakao':
        messages.success(request, "카카오톡 로그인 계정은 비밀번호가 없습니다.")
        return redirect('accounts:profile_edit')

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
