from django.urls import path
from .views import AddNewArticle, AddNewReview_View

app_name = 'userPanel_module'

urlpatterns = [
    path('profile/add_article/', AddNewArticle.as_view(), name="add_new_article"),
    path('profile/review_article/<str:review_id>/', AddNewReview_View.as_view(), name="add_new_review")
]