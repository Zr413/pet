import datetime
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from pet_proj_dj import settings
from blog.models import Categories, News


# Рассылка новостей за последнюю неделю
@shared_task
def send_email_every_monday():
    #  Your job processing logic here...
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    news = News.objects.filter(time__gte=last_week)
    categories = set(news.values_list('new_cat__title', flat=True))
    subscribes = set(Categories.objects.filter(title__in=categories).values_list('subscribes__email', flat=True))
    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'news': news,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribes,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


# Отправка уведомления подписчику, в случае добавления новости
@shared_task
def send_notifications(preview, pk, title, subscribes):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribes,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
