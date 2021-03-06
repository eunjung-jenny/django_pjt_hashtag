# Hashtag 기능이 있는 게시판

## 1. 설계

### 1) 모델

#### accounts.User

- username
- followers (ManyToManyField(User, related_name='follows'))

#### community.Article

- title
- content
- creator (FK(User))
- created_at
- updated_at
- like_users (ManeToManyField(User, related_name='like_articles))

#### community.Comment

- content
- creator (FK(User))
- article (FK(Article))
- created_at
- updated_at

#### Hashtag

- tag_name
- has_articles (ManyToManyField(Article, related_name='has_hashtags'))

### 2) View / Template

#### navbar

- Logo (-> 'community:index')
- Join, Login, User(dropdown: profile, settings, logout)

#### 'community:index'

- article (bootstrap-card) (-> 'community:detail')

#### 'community:detail'

- 글 내용 ( creator -> 'accounts:profile')
- 좋아요 (-> 모달: 좋아요 한 사람)
- 댓글 ( username -> 'accounts:profile')
- 태그 (-> 'community:hashtag')

#### 'community:hashtag'

- **'community:index' 와 템플릿 공유**
- article (bootstrap-card) (-> 'community:detail')

#### 'accounts:profile'

- 팔로우/팔로잉 (-> 모달: 팔로우/팔로잉 한 사람)
- 작성한 글 (-> 'community:detail')
- 계정 설정/삭제

## 2. 구현

### 1) accounts

- [x] 회원가입
- [x] 로그인
  - [] 아이디 기억하기
  - [] 로그인 쿠키
- [x] 회원정보 변경
  - [] 비밀번호 재확인
  - [] 프로필 사진
- [] 비밀번호 초기화
- [x] 비밀번호 변경
- [x] 로그아웃
- [x] 계정 삭제
- [] 계정 비활성화
- [x] 팔로우/팔로잉
  - [x] 팔로워/팔로우 유저 목록
- [x] 작성한 글/ 좋아한 글 목록
- [] 메세지 주고 받기
- [] 유저 태그 (@username)
- [] 푸시 알림

### 2) community

- [x] 게시글
  - [x] 조회
    - [] 팔로우 하는 사람의 글 우선 보여주기
    - [] 조회수
    - [] 새로운 글 표시
  - [x] 작성
  - [x] 수정
  - [x] 삭제
  - [] 글 공유 기능
- [x] 좋아요
  - [x] 좋아요/좋아요 취소
  - [x] 좋아요 수 카운팅
  - [x] 좋아요 한 유저 목록
- [] 댓글
  - [x] 작성
  - [] 수정
  - [x] 대댓글
  - [x] 무한 댓글
  - [] 새로운 댓글 있는지 표시
- [x] 해시태그
  - [x] 작성
  - [x] 수정
  - [x] 검색
    - [x] 검색어와 정확히 일치하는 글 검색
    - [] 검색어를 포함하는 글 검색
  - [] 태그 입력 방식 변경 (글 내에서 바로 추출)
- [] 북마크
- [] 이미지 업로드
- [] 쿼리 최적화

- [] development, production 설정 분리

### 3) 스타일링

- [] nav 고치기

### 4) 노트

#### (1) index 페이지에서 좋아요 를 눌렀을 때와 detail 페이지에서 좋아요 를 눌렀을 때 redirect 페이지를 다르게 주고 싶다.

- `request.META.get('HTTP_REFERER')` 에서 직전 url 을 문자열 타입으로 받을 수 있음 / 외부 사이트에서 넘어온 경우에는 None 값 반환
- ` resolve_url('community:index')``request.resolver_match.url_name ` 과 반대되는 기능

  - `from django.shortcuts import resolve_url`

- 직전 url 과 urlpatterns 에 정의된 url명을 비교하여 같은 기능을 수행한 뒤 다른 페이지로 리다이렉션 가능

- challenge) 외부에서 넘어오는 경우, 직전 url 을 받아올 수 없으므로 에러 발생 => None 값일 경우, index 또는 detail 페이지로 분기시켜 줄 필요가 있음

- challenge) login 되어 있지 않은 경우, 로그인 페이지로 넘어갔다가 해당 url 로 다시 접근하게 되는데 이 경우 직전 url 이 'accounts:login' 에 해당함 => index 또는 detail 페이지로 분기시켜 줄 필요가 있으며, 좋아요 카운팅을 해 줄 것인지에 대해 고려해야 함

- **배포시 host 가 달라지는 부분 고려해야 함**

#### (2) 해로쿠 배포

- [완숙의 에그머니 따라하기](https://egg-money.tistory.com/115)

- **주의** url 인식하는 기능이 구현되어 있는 경우에는 개발 환경에서와 배포 환경에서의 url 이 달라지므로 이를 고려해줘 함
- **주의** '.env' 를 통한 환경 설정이 있는 경우 `heroku config:set [변수명]=[값]` 으로 설정해주어야 하며 설정되어 있는 값들은 `heroku config` 로 확인 가능

#### (3) 대댓글

- 처음에는 대댓글 모델을 따로 만들어줬다.
- 댓글이랑 다를 바 없기 때문에 댓글 모델이랑 합칠 수도 있을 거 같다.
  - 자기 자신을 참조할 때는 `models.ForeignKey("self", on_delete=[옵션])` 과 같이 "self" 옵션을 사용
- 댓글이랑 모델을 합쳐주고 나니 대대대대댓글을 하기도 더 쉬워진 거 같다.
  - 모든 댓글 인스턴스에서 대댓글이 있는지 `child_comments` 로 조회할 수 있기 때문에 이를 활용해 대댓글이 있을 경우 django template language 의 `{% include '_comment.html' %}` 을 계속 이어붙여 주는 방식으로 구현이 가능할 거 같다. => 성공

#### (4) Secret key 보안

- 프라이빗으로 관리하던 레포를 퍼블릭 레포로 변경하게 되면서 과정에서 secret key 가 노출되었음
- [Welcome to Django-environ’s documentation!](https://django-environ.readthedocs.io/en/latest/) 를 참고하여 secret key 를 변경하고 숨김파일로 관리하는데 성공
- 실제 서비스를 운영 중인 웹/앱 이라면 1) 세션 정보 2) 토큰 3) 메세지 4) 댓글 (`django.contrib.comments` 사용시) 등의 기능에서 secret key 를 사용하기 때문에 변경 시점에 관련 정보들이 초기화되어 오류가 있을 수 있다.

#### (5) Debug panel

- [django-debug-toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/installation.html)

#### (6) fetch 를 이용한 ajax 통신 (=> 좋아요 기능 수정)

- [promise 는 어려워](https://stackoverflow.com/questions/37555031/why-does-json-return-a-promise)
  - fetch 를 하면 서버에서 헤더가 도착하자마자 response 를 받게 되고, 이 때 아직 body 전체가 로딩되기 이전이라 `fetch(~~).then(res => res.json())` 를 했을 때 `res.json()` 은 또 다른 promise 가 됨.
  - `then` 을 두 번 사용하거나 `then` 과 `async ... await` 를 함께 사용하여 해결
- 해로쿠 배포시 복잡했던 url 인식 이슈가 사라짐
- 주소창에 해당 api 요청 주소를 입력하여 접근시 json 데이터가 보여지는 문제가 있었음
  - 1. 일단은 `@require_POST` 를 통해 해결
    - csrf token 을 넘겨줘야 하는 이슈가 있었는데 토큰은 `document.cookie` 에서 찾을 수 있고 이를 `header` 에 함께 보내줘야 함
  - 2. url 을 기존의 `/community/<pk>/like/` 로 만들었는데 `/api/v1/like/` 이런 식으로 분리해야 하는건가?
  - 3. DRF 사용하여 api server 구축하면더 편리해지는가?
