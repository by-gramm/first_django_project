# 🎂 생일 축하 프로젝트

Django의 기본 MTV 패턴도 익히고, 친구의 생일도 축하해 주는 일석이조의 프로젝트

<br><br>

> ## 홈페이지 주소

(추가 예정)

<br>

> ## 프로젝트 기간

2021.04.11 ~ 2021.04.27

<br>

> ## 구현 내용

- User 모델

  - 회원가입 (+ 자동 로그인) / 회원 탈퇴
  - 회원정보 수정 / 비밀번호 변경
  - 로그인 / 로그아웃
  - 카카오 소셜 로그인 (OAuth 2.0 기반 카카오 로그인 API 연동)
  
- Post 모델 C/R/U/D 구현

- Comment 모델 C/R/D 구현

<br>

> ## ✏ 기억할 만한 코드

### UNIQUE 무결성 제약조건을 가지는 이메일 필드 구현

<br>

카카오 소셜 로그인 기능을 추가하기 전의 User 모델은 아래와 같았다. <br>

AbstractUser 클래스를 상속받은 새로운 User 모델을 만들고, <br>

생일인 친구와의 관계를 나타내는 `relation_with_minki` 필드와 `profile_image` 필드를 추가했다.

```python
class User(AbstractUser):

    RELATION_CHOICES = (
        (0, '가족 혹은 친척'),
        (1, '친구'),
        (2, '지인'),
        (3, '누군지 모르는')
    )
    
    profile_image = ProcessedImageField(
        blank=True,
        upload_to='profile_image/%Y/%m/%d',
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 80},
        help_text='따로 지정하지 않으면 기본 이미지로 저장됩니다.',
    )
    
    relation_with_minki = models.SmallIntegerField(choices=RELATION_CHOICES, default=2)


    @property
    def profile_image_url(self):
        if self.profile_image:
            return self.profile_image.url
        else:
            return "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"
```

<br>

여기에 카카오 소셜 로그인 기능을 추가하면서, 로그인 방법을 나타내는 `login_method` 필드를 새로 추가했다.

```python
class User(AbstractUser):
    (중략)

    LOGIN_CHOICES = (
        ("email", "Email"),
        ("kakao", "Kakao"),
    )

    login_method = models.CharField(max_length=6, choices=LOGIN_CHOICES, default="email")
```

<br>

카카오 유저 모델의 경우, 사용자 이름에는 `unique=True` 조건이 없다. 그래서 사용자 이름을 기준으로 회원 가입 여부를 판단할 수는 없다. <br>

그래서 `unique=True` 조건이 있는 이메일을 기준으로 회원 가입 여부를 판단하여, 중복 가입을 방지했다.

```python
def kakao_callback(request):
    (중략)
    
    # 카카오 유저 정보에서 가져온 이메일과 같은 이메일을 쓰는 유저가 있는 경우,
    # 1) 그 유저가 카카오 가입 유저가 아니라면 에러 메세지를 보여주고,
    # 2) 카카오 가입 유저라면 바로 로그인시킨다.
    user = User.objects.filter(email=email).first()
    if not user:
        ```카카오 계정 정보를 바탕으로 새로운 회원 정보 생성하는 부분```

    if user.login_method == 'email':
        messages.error(request, "해당 계정은 이미 가입되어 있습니다. 사용자 이름/비밀번호로 로그인해주세요.")
        return redirect('accounts:login')
        
    user.set_unusable_password()
    user.save()
    messages.success(request, "카카오로 로그인했습니다.")
    auth_login(request, user)
```

<br>

그런데 앞서 정의한 User 모델의 이메일 필드는 `unique=True` 조건이 없다. <br>

User 모델이 AbstractUser 클래스를 상속받는데, AbstractUser 클래스의 이메일 필드에 `unique=True` 조건이 없기 때문이다. <br>

그렇다면 아래와 같이 `unique=True` 조건을 포함한 email 필드를 재정의해야 할 것이다.

```python
 email = models.EmailField(max_length=100, unique=True)
```

<br>

그런데 AbstractUser 클래스의 이메일 필드에는 `blank=True` 조건이 있다. 이는, 원래는 이메일 주소를 쓰지 않고도 회원가입이 가능했다는 것을 의미한다.

처음부터 이메일 필드 입력을 필수로 지정했다면 문제가 없겠지만,

이미 이메일 주소를 작성하지 않고 가입한 회원들이 있면, 이면, 이메일 필드에 `blank=True` 조건을 추가해야 한다.

```python
  email = models.EmailField(max_length=100, unique=True, blank=True, help_text="적지 않아도 괜찮습니다.")
```

<br>

문제는 폼에서 이메일 주소를 빈 값으로 입력받으면 빈 문자열로 저장되는데, 빈 문자열끼리는 같은 값으로 인식되어 `unique=True` 조건에 걸린다는 것이다.

이처럼 `blank=True` 조건과 `unique=True` 조건이 충돌하는 경우, `null=True` 조건을 추가함으로써 해결할 수 있다.

null값은 여러 필드가 동시에 가지더라도 유일성 조건에 걸리지 않기 때문이다.

```python
 email = models.EmailField(max_length=100, unique=True, blank=True, null=True, help_text="적지 않아도 괜찮습니다.")
```

<br>

하지만 여전히 문제는 해결되지 않는다. 

CharField, TextField, EmailField와 같은 문자열 기반 필드에서는 `null=True` 조건이 있더라도,

폼에서 빈 값을 입력받으면 DB에 빈 문자열로 저장되기 때문이다.

따라서 회원 가입시 이메일 필드에 빈 문자열을 입력받은 경우, null값으로 바꾸어 주어야 한다.

**그래서 유효성 검사를 수행하는 clean() 메서드 내에서 빈 문자열을 null값으로 바꾸어 줌으로써,**

**폼에서 빈 문자열을 입력받더라도 유일성 조건에 걸리지 않게 했다.**

```python
class User(AbstractUser):
    (중략)

    # unique=True 조건을 만족시키기 위해,
    # 입력하지 않은 이메일 필드의 값을 null값으로 바꾼다.
    def clean(self):
        if self.email == "":
            self.email = None
```
