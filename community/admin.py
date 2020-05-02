from django.contrib import admin
from .models import Article, Comment, Hashtag

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'creator')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'article', 'creator', 'content')

class HashtagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'tag')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Hashtag, HashtagAdmin)


