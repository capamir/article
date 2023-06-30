from django.contrib import admin
from .models import *

# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ["user", "title", "created"]

class ReviewAdmin(admin.ModelAdmin):
    list_display = ["owner", "article","created"]
    
    def get_queryset(self, request):
        # Filtering by specific role
        queryset = super().get_queryset(request)
        queryset = queryset.filter(owner__role='proffesor')
        return queryset

admin.site.register(ArticleModel, ArticleAdmin)
admin.site.register(ReviewModel, ReviewAdmin)