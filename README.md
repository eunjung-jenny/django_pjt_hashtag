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
- [x] 해시태그
  - [x] 작성
  - [x] 수정
  - [x] 검색
    - [x] 검색어와 정확히 일치하는 글 검색
    - [] 검색어를 포함하는 글 검색
- [] 북마크
- [] 이미지 업로드

### 3) 스타일링

- [] nav 고치기

### 4) 노트

- index 페이지에서 좋아요 를 눌렀을 때와 detail 페이지에서 좋아요 를 눌렀을 때 redirect 페이지를 다르게 주고 싶다.

  - `request.META.get('HTTP_REFERER')` 에서 직전 url 을 문자열 타입으로 받을 수 있음 / 외부 사이트에서 넘어온 경우에는 None 값 반환
  - ` resolve_url('community:index')``request.resolver_match.url_name ` 과 반대되는 기능

    - `from django.shortcuts import resolve_url`

  - 직전 url 과 urlpatterns 에 정의된 url명을 비교하여 같은 기능을 수행한 뒤 다른 페이지로 리다이렉션 가능

  - challenge) 외부에서 넘어오는 경우, 직전 url 을 받아올 수 없으므로 에러 발생 => None 값일 경우, index 또는 detail 페이지로 분기시켜 줄 필요가 있음

  - challenge) login 되어 있지 않은 경우, 로그인 페이지로 넘어갔다가 해당 url 로 다시 접근하게 되는데 이 경우 직전 url 이 'accounts:login' 에 해당함 => index 또는 detail 페이지로 분기시켜 줄 필요가 있으며, 좋아요 카운팅을 해 줄 것인지에 대해 고려해야 함
