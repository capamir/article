from django.contrib import admin
from .models import *

# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ["user", "title", "created"]
    raw_id_fields = ('user',)
    search_fields = ('title',)
    ordering = ('created',)
    readonly_fields = ('title', 'description')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ["owner", "article", "created"]
    raw_id_fields = ('owner', 'article')
    ordering = ('created',)


admin.site.register(ArticleModel, ArticleAdmin)
admin.site.register(ReviewModel, ReviewAdmin)