from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.index, name='index'),
    path('post/', views.post, name='post'),
    path('<int:article_pk>/', views.detail, name='detail'),
    path('<int:article_pk>/like/', views.like, name='like'),
    path('<int:article_pk>/edit/', views.edit, name='edit'),
    path('<int:article_pk>/delete/', views.delete, name='delete'),
    path('search/', views.search, name='search'),
    path('<int:article_pk>/comment_create/', views.comment_create, name='comment_create'),
    path('<int:article_pk>/child_comment_create/<int:comment_pk>/', views.child_comment_create, name='child_comment_create'),
]