from django.contrib import admin
from .models import Post, Tag, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'date_pub', 'tags_list')
    list_display_links = ('title', 'slug')
    search_fields = ('title', 'body')

    def tags_list(self, obj):
        return ", ".join([tag.title for tag in obj.tags.all()])

    tags_list.short_description = "Теги"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'created_at')
    search_fields = ('author', 'text')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    list_display_links = ('title', 'slug')
    search_fields = ('title',)
