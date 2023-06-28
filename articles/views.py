from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class ArticlesView(TemplateView):
    template_name = 'articles/articles.html'
    