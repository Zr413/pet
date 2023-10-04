from django.contrib.auth.models import User

from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from .models import Author, NewsCategories
from .tasks import send_notifications


# Создание имени автора по умолчанию от имени пользователя
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        full_name = f"{instance.first_name} {instance.last_name}"
        instance.author = Author.objects.create(full_name=full_name, user_id=instance.id)
        instance.author.save()


# Создание уведомления подписчику, в случае добавления новости
@receiver(m2m_changed, sender=NewsCategories)
def notify_about_new_news(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.new_cat.all()
        subscribes: list[str] = []
        for cat in categories:
            subscribes += cat.subscribes.all()
        subscribes = [s.email for s in subscribes]
        send_notifications(instance.preview(), instance.pk, instance.title, subscribes)
