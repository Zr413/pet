from django import forms
from django.forms.utils import ErrorList

from .models import News, Comment
from django.core.exceptions import ValidationError


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        image = forms.ImageField()
        fields = [
            'image',
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

    # Добавление метода для валидации темы, проверка начала строки
    def clean_title(self):
        title = self.cleaned_data["title"]
        if title[0].islower():
            raise ValidationError(
                "Тема не должна начинаться со строчной буквы"
            )
        return title

    # Добавление метода для валидации статьи, проверка начала строки
    def clean_article(self):
        article = self.cleaned_data["article"]
        if article[0].islower():
            raise ValidationError(
                "Статья не должна начинаться со строчной буквы"
            )
        return article

    # Добавление метода для валидации изображения
    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image.content_type not in ['image/jpeg', 'image/png']:
                raise forms.ValidationError("Тип файла не поддерживается")
            return image
        raise forms.ValidationError("Не удалось прочитать файл")


# Форма для комментариев к статье
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class': 'textarea', 'placeholder': 'Write your comment here...'})
