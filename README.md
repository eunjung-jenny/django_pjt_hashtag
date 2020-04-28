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
- [x] 회원정보 변경
- [] 비밀번호 초기화
- [x] 비밀번호 변경
- [x] 로그아웃
- [x] 계정 삭제
- [x] 팔로우/팔로잉
  - [x] 팔로워/팔로우 유저 목록
- [x] 작성한 글/ 좋아한 글 목록

### 2) community

- [x] 게시글
  - [x] 조회
  - [x] 작성
  - [x] 수정
  - [x] 삭제
- [x] 좋아요
  - [x] 좋아요/좋아요 취소
  - [x] 좋아요 수 카운팅
  - [x] 좋아요 한 유저 목록
- [] 댓글
- [x] 해시태그
  - [x] 작성
  - [x] 수정
  - [x] 검색

### 3) 스타일링

- []
