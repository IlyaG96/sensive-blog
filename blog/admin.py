from django.contrib import admin
from blog.models import Post, Tag, Comment


@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    raw_id_fields = ('post', 'author')


@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    raw_id_fields = ('author', 'likes', 'tags')


admin.site.register(Tag)
