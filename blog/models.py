from django.db import models
from datetime import datetime
from django.db.models import Sum
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.urls import reverse


# Таблица с сущностью автора
class Author(models.Model):
    full_name = models.CharField(max_length=150)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    # Обновление рейтинга автора на основании лайков и дизлайков
    def update_rating(self):
        news_rat = News.objects.aggregate(rat_a=Sum('rating'))
        n_rat = news_rat.get('rat_a')

        comment_rat = Comment.objects.aggregate(rat_c=Sum('rating'))
        c_rat = comment_rat.get('rat_c')

        self.rating = n_rat * 3 + c_rat
        self.save()

    def __str__(self):
        return f'{self.user}, {self.full_name}, {self.rating}'


# Промежуточная таблица для новостей и категорий
class NewsCategories(models.Model):
    new_key = models.ForeignKey('News', on_delete=models.CASCADE)
    cat_key = models.ForeignKey('Categories', on_delete=models.CASCADE)


class Subscription(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='subscriptions')
    category = models.ForeignKey(to='Categories', on_delete=models.CASCADE, related_name='subscriptions')

    class Meta:
        db_table = 'blog_categories_subscribes'


# Категории
class Categories(models.Model):
    title = models.CharField(max_length=250, unique=True)
    subscribes = models.ManyToManyField(User, related_name='categories', through='Subscription')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title.title()


# Новости
class News(models.Model):
    time = models.DateTimeField(auto_now=False, auto_now_add=True)
    title = models.CharField(max_length=50)
    article = models.TextField()
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новости'),
        (ARTICLE, 'Статья'),
    )
    article_or_news = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=NEWS)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    new_cat = models.ManyToManyField(Categories, through='NewsCategories')
    rating = models.IntegerField(blank=False, default=0)

    # Время добавления
    def date(self):
        # self.time = datetime.strftime('%d.%m.%Y')
        self.time = datetime.now()
        self.save()

    # Лайки и дизлайки новостей
    # def like(self, user):
    #     user_rating, created = UserRating.objects.get_or_create(user=user, news=self, defaults={'rating': 1})
    #     if created:
    #         self.rating += 1
    #         self.save()
    #
    # def dislike(self, user):
    #     user_rating, created = UserRating.objects.get_or_create(user=user, news=self, defaults={'rating': -1})
    #     if created:
    #         self.rating -= 1
    #         self.save()

    def like(self, user):
        user_rating, created = UserRating.objects.get_or_create(user=user, news=self)
        if created or user_rating.rating != 1:
            self.rating += 1
            self.save()
            user_rating.rating = 1
            user_rating.save()

    def dislike(self, user):
        user_rating, created = UserRating.objects.get_or_create(user=user, news=self)
        if created or user_rating.rating != -1:
            self.rating -= 1
            self.save()
            user_rating.rating = -1
            user_rating.save()

    # Превью новости
    def preview(self):
        if len(self.article) > 124:
            return f'{self.article[:124]}...'
        return f'{self.article}'

    def __str__(self):
        return f'{self.time.date()}, {self.title.title()}: {self.article}, {self.title.title()}: {self.new_cat}'

    def get_absolute_url(self):
        return reverse('news-details', args=[str(self.id)])


# Таблица с комментариями
class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time = models.DateTimeField(auto_now=False, auto_now_add=True)
    rating = models.IntegerField(blank=False, default=0)

    # Время добавления
    def date(self):
        self.time = datetime.now()
        self.save()

    # Лайки и дизлайки новостей
    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.time.date()}, {self.user}, {self.text}, {self.rating}'

    def get_absolute_url(self):
        return reverse('news-details', args=[str(self.news.id)])


class UserRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    rating = models.IntegerField(blank=False, default=0)

    class Meta:
        unique_together = ('user', 'news')
