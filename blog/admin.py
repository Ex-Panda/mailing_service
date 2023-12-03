from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'date_creation', 'is_publication',)
    list_filter = ('date_creation',)
    search_fields = ('title',)
    fields = ('title', 'content', 'preview', 'is_publication')

