from datetime import timedelta

from celery import shared_task

from django.utils.timezone import now

from users.models import User


@shared_task
def last_login_check():
    users = User.objects.filter(is_active=True)
    current_date = now()
    for user in users:
        if user.last_login and current_date - user.last_login > timedelta(days=30):
            user.is_active = False
            user.save()
        elif current_date - user.date_joined > timedelta(days=30):
            user.is_active = False
            user.save()
