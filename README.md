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
