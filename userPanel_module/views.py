from django.shortcuts import render
from  django.views import View
# Create your views here.
from django.views.generic import TemplateView,ListView
from articles.models import Article,Review
from articles.forms import ArticleForm
from django.shortcuts import redirect,reverse

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

class AddNewArticle(View):
    def get(self, request):
        article_form = ArticleForm()
        context = {
            'article_form' : article_form,
        }
        return render(request, "userPanel_module/student_view/add_new_article.html", context)
    def post(self, request):
        article_form = ArticleForm(request.POST)
        if(article_form.is_valid()):
            cd = article_form.cleaned_data
            get_user = request.user
            title = cd["title"]
            description = cd["description"]
            file = cd["file"]
            new_article = Article.objects.create(
                title=title,
                description=description,
                file=file,
                owner=get_user,
            )
            new_article.save()
            return redirect(reverse("account:account"))
        context = {
            'article_form' : article_form,
        }
        return render(request, "userPanel_module/student_view/add_new_article.html", context)
