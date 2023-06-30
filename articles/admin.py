from django.contrib import admin
from .models import *

# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ["user", "title"]

class ReviewAdmin(admin.ModelAdmin):
    list_display = ["owner", "article","created"]

admin.site.register(ArticleModel, ArticleAdmin)
admin.site.register(ReviewModel, ReviewAdmin)