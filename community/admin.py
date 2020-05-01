from django.contrib import admin
from .models import Article, Comment, ChildComment, Hashtag

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'creator')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'article', 'creator', 'content')

class ChildCommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'parent_comment', 'creator', 'content')

class HashtagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'tag')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ChildComment, ChildCommentAdmin)
admin.site.register(Hashtag, HashtagAdmin)


