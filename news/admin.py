from django.contrib import admin

from news.models import Category, Post, Comment, Tag
from common.models import Contact


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'title')


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Contact)
admin.site.register(Tag)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'id', 'body', 'created_at', 'is_active']


admin.site.register(Comment, CommentAdmin)