from django.contrib import admin
from .models import Article, Review
from django.utils.html import format_html

# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ["article_name" ,"article_owner", "created","updated" ,"is_view", "admin_last_view"]
    list_filter = ['is_view',]
    raw_id_fields = ('owner', 'judges',)
    search_fields = ('title','admin_last_view','created','updated',)
    ordering = ('created','updated','is_view', 'admin_last_view',)
    readonly_fields = ('is_view','admin_last_view','updated')
    
    @admin.display
    def article_owner(self, obj:Article):
        user_change_url = f'/admin/account/user/{obj.owner.id}/change/'
        
        return format_html("<a href='{url}'>{name}</a>",url=f'{user_change_url}', name=obj.owner.full_name)    
    
    @admin.display
    def article_name(self, obj:Article):
        article_change_url = f'/admin/articles/article/{obj.id}/change/'
        
        return format_html("<a href='{url}'>{name}</a>",url=f'{article_change_url}', name=obj.title)    

class ReviewAdmin(admin.ModelAdmin):
    list_display = ["judge_by", "article_name","article_owner","created",'updated', 'article_score']
    raw_id_fields = ('owner', 'article')
    ordering = ('created',)
    readonly_fields = ('created','updated',)

    @admin.display
    def article_owner(self, obj:Review):
        user_change_url = f'/admin/account/user/{obj.article.owner.id}/change/'
        
        return format_html("<a href='{url}'>{name}</a>",url=f'{user_change_url}', name=obj.article.owner.full_name)
    
        # return obj.article.owner.full_name
    @admin.display
    def judge_by(self, obj:Review):
        return obj.owner.user.full_name
    
    @admin.display
    def article_name(self, obj:Review):
        article_change_url = f'/admin/articles/article/{obj.article.id}/change/'
        
        return format_html("<a href='{url}'>{name}</a>",url=f'{article_change_url}', name=obj.article)
    @admin.display
    def article_score(self, obj:Review):
        return f"{obj.score} / 100"
        

admin.site.register(Article, ArticleAdmin)
admin.site.register(Review, ReviewAdmin)