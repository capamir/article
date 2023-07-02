from django.contrib import admin
from .models import Article, Review

# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ["owner", "title", "created"]
    raw_id_fields = ('owner', 'judges')
    search_fields = ('title',)
    ordering = ('created',)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ["owner", "article", "created"]
    raw_id_fields = ('owner', 'article')
    ordering = ('created',)


admin.site.register(Article, ArticleAdmin)
admin.site.register(Review, ReviewAdmin)