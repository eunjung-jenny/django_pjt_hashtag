from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.index, name='index'),
    path('post/', views.post, name='post'),
    path('<int:article_pk>/', views.detail, name='detail'),
    path('<int:article_pk>/like/', views.like, name='like'),
]