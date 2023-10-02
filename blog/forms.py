from django import forms
from django.forms.utils import ErrorList

from .models import News
from django.core.exceptions import ValidationError


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = [
            'title',
            'article',
            'new_cat',
        ]

    def __init__(
            self,
            data=None,
            files=None,
            auto_id="id_%s",
            prefix=None,
            initial=None,
            error_class=ErrorList,
            label_suffix=None,
            empty_permitted=False,
            instance=None,
            use_required_attribute=None,
            renderer=None,
    ):
        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance,
                         use_required_attribute, renderer)
        self.News = None

    # Валидация поля тема
    def clean(self):
        cleaned_data = super().clean()
        article = cleaned_data.get("article")
        if article is not None and len(article) < 3:
            raise ValidationError({
                "article": "Статья не может быть менее 10 символов."
            })

        title = cleaned_data.get("title")
        if title == article:
            raise ValidationError(
                "Текст темы и статьи не должны быть идентичны."
            )

        return cleaned_data

    def clean_title(self):
        title = self.cleaned_data["title"]
        if title[0].islower():
            raise ValidationError(
                "Тема не должна начинаться со строчной буквы"
            )
        return title

    def clean_article(self):
        article = self.cleaned_data["article"]
        if article[0].islower():
            raise ValidationError(
                "Статья не должна начинаться со строчной буквы"
            )
        return article
