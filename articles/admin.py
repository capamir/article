from django.contrib import admin
from .models import Article, Review, Notification_Manager

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

class Notification_Manager_Admin(admin.ModelAdmin):
    list_display = ["article", "created"]
    raw_id_fields = ('article',)
    ordering = ('created',)
        

admin.site.register(Article, ArticleAdmin)
admin.site.register(Review, ReviewAdmin)

admin.site.register(Notification_Manager, Notification_Manager_Admin)