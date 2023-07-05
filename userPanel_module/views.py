from django.shortcuts import render
from  django.views import View
# Create your views here.
from django.views.generic import TemplateView, ListView
from articles.models import Article, Review
from articles.forms import ArticleForm, ReviewForm
from django.shortcuts import redirect, reverse

# === STUDENT VIEW ===

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
        article_form = ArticleForm(request.POST, request.FILES)
        if(article_form.is_valid()):
            cd = article_form.cleaned_data
            get_user = request.user
            title = cd["title"]
            description = cd["description"]
            file = request.FILES["file"]
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


# === PROFESSOR VIEW ===
class ProfessorView(TemplateView):
    template_name = 'userPanel_module/professor_view/professor_view.html'
    def get_context_data(self, **kwargs):
        context = super(ProfessorView, self).get_context_data()
        context['profile'] = self.request.user.profile
        return context

class ProfessorArticles_for_review_View(ListView):
    model = Review
    template_name = 'userPanel_module/professor_view/Articles_for_review.html'

    def get_queryset(self):
        query = super(ProfessorArticles_for_review_View, self).get_queryset()
        return query

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProfessorArticles_for_review_View, self).get_context_data()
        professor = self.request.user.professor_set.first()
        reviews = Review.objects.filter(owner=professor, body__exact='')
        context['reviews'] = reviews
        return context

class AddNewReview_View(View):
    def get(self, request, review_id):
        review_form = ReviewForm()
        find_review_obj = Review.objects.get(id=review_id)
        context = {
            'review_form': review_form,
            'review': find_review_obj
        }
        return render(request, 'userPanel_module/professor_view/add_new_review.html', context)
    def post(self, request, review_id):
        review_form = ReviewForm(request.POST)
        find_review_obj = Review.objects.get(id=review_id)

        if(review_form.is_valid()):
            cd = review_form.cleaned_data
            body = cd['body']
            find_review_obj.body = body
            find_review_obj.save()
            return redirect(reverse("account:account"))
        context = {
            'review_form': review_form,
            'review': find_review_obj
        }
        return render(request, 'userPanel_module/professor_view/add_new_review.html', context)

class ProfessorLast_reviews_View(ListView):
    model = Review
    template_name = 'userPanel_module/professor_view/last_reviews.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProfessorLast_reviews_View, self).get_context_data()
        professor = self.request.user.professor_set.first()
        reviews = Review.objects.filter(owner=professor).exclude(body__exact='')
        context['reviews'] = reviews
        return context