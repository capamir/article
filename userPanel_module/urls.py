from django.urls import path
from .views import AddNewArticle

app_name = 'userPanel_module'

urlpatterns = [
    path('profile/add_article/', AddNewArticle.as_view(), name="add_new_article")
]