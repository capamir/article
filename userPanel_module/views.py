from django.shortcuts import render
from  django.views import View
# Create your views here.
from django.views.generic import TemplateView,ListView
from articles.models import Article

class StudentView(TemplateView):
    template_name = 'userPanel_module/student_view/studentView.html'

    def get_context_data(self, **kwargs):
        context = super(StudentView, self).get_context_data()
        context['profile'] = self.request.user.profile
        return context

class StudentArticlesView(ListView):
    model = Article
    template_name = 'userPanel_module/student_view/Article_list_view.html'

    def get_queryset(self):
        query = super(StudentArticlesView, self).get_queryset()
        return query

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StudentArticlesView, self).get_context_data()
        user = self.request.user
        articles = Article.objects.filter(owner=user)
        context['articles'] = articles
        return context