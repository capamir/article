from django.urls import path
from .views import AddNewArticle, AddNewReview_View, ProfessorLast_reviews_View,EditReview_View, showArticle

app_name = 'userPanel_module'

urlpatterns = [
    path('profile/add_article/', AddNewArticle.as_view(), name="add_new_article"),
    path('profile,show_article/<str:article_id>', showArticle.as_view(), name="show_article"),
    path('profile/add_review/<str:review_id>/', AddNewReview_View.as_view(), name="add_new_review"),
    path('profile/edit_review/<str:review_id>/', EditReview_View.as_view(), name="edit_review"),
    path('profile/last_reviews/', ProfessorLast_reviews_View.as_view(), name="last_reviews"),
]