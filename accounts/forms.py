import allauth.account.forms
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.core.mail import send_mail, EmailMultiAlternatives, mail_admins

from blog.models import Author


# Форма регистрации
class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


# Привязка группы "authors" по умолчанию к зарегистрированному пользователю
class CustomSignupForm(SignupForm):
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    def save(self, request):
        user = super().save(request)
        authors = Group.objects.get(name="authors")
        # send_mail(
        #     subject='Добро пожаловать в наш интернет-магазин!',
        #     message=f'{user.username}, вы успешно зарегистрировались!',
        #     from_email=None,  # будет использовано значение DEFAULT_FROM_EMAIL
        #     recipient_list=[user.email],
        # )
        subject = 'Добро пожаловать в наш интернет-магазин!'
        text = f'{user.username}, вы успешно зарегистрировались на сайте!'
        html = (
            f'<b>{user.username}</b>, вы успешно зарегистрировались на '
            f'<a href="http://127.0.0.1:8000/products">сайте</a>!'
        )
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[user.email]
        )
        msg.attach_alternative(html, "text/html")
        msg.send()
        mail_admins(
            subject='Новый пользователь!',
            message=f'Пользователь {user.username} зарегистрировался на сайте.'
        )
        if not request.user.groups.filter(name='authors').exists():
            authors.user_set.add(user)
            user.groups.add(authors)
        return user

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
        )


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('avatar', 'full_name', 'birth_date')

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not full_name:
            raise forms.ValidationError("Поле 'full_name' не может быть пустым")
        names = full_name.split()
        if len(names) < 2:
            raise forms.ValidationError("Пожалуйста, введите ваше полное имя (имя и фамилию)")
        return full_name

    def save(self, commit=True):
        author = super(AuthorForm, self).save(commit=False)
        full_name = self.cleaned_data['full_name']
        names = full_name.split()
        author.user.first_name = names[0]
        if len(names) > 1:
            author.user.last_name = " ".join(names[1:])
        author.full_name = full_name

        if commit:
            author.user.save()
            author.save()

        return author

    # def save(self, commit=True):
    #     author = super(AuthorForm, self).save(commit=False)
    #     author.full_name = self.cleaned_data['full_name']
    #
    #     if commit:
    #         author.save()
    #
    #     return author
