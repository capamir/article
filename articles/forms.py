from django import forms
from django.core.validators import FileExtensionValidator

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
        max_length=500,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "id": "article_description",
            }
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
