from django import forms
from django.core.validators import FileExtensionValidator,MaxValueValidator,MinValueValidator
from ckeditor.widgets import CKEditorWidget

class ArticleForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ArticleForm, self).__init__(*args, **kwargs)

    title = forms.CharField(
        label="Title",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "article_title",
            }
        ),
    )
    description = forms.CharField(
        label="description",
        widget=CKEditorWidget(
            attrs={
                "class": "form-control",
                "id": "article_description",
            },
            config_name='article_description',
        ),
    )
    file = forms.FileField(
        label="file",
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
                "id": "article_file",
            }
        ),
        validators= [
            FileExtensionValidator(["pdf"], message="File Type is not correct !"),
        ]
    )

class EditArticleForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(EditArticleForm, self).__init__(*args, **kwargs)

    title = forms.CharField(
        label="Title",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "article_title",
            }
        ),
    )
    description = forms.CharField(
        label="description",
        widget=CKEditorWidget(
            attrs={
                "class": "form-control",
                "id": "article_description",
            },
            config_name='article_description',
        ),
    )
    file = forms.FileField(
        label="file",
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
                "id": "article_file",
            }
        ),
        required=False,
        validators= [
            FileExtensionValidator(["pdf"], message="File Type is not correct !"),
        ]
    )

class ReviewForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ReviewForm, self).__init__(*args, **kwargs)

    score = forms.IntegerField(
        label='score',
        validators=[
            MaxValueValidator(100, message="score should be between 0 and 100 !"),
            MinValueValidator(0, message="score should be between 0 and 100 !")
        ]
    )

    body = forms.CharField(
        label="body",
        max_length=500,
        # widget=forms.Textarea(
        #     attrs={
        #         "class": "form-control",
        #         "id": "review_body",
        #     }
        # ),
        widget=CKEditorWidget(
            attrs={
                "class": "form-control",
                "id": "review_body",
            }
        ),
    )
