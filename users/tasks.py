from datetime import timedelta

from celery import shared_task

from django.utils.timezone import now

from users.models import User


@shared_task
def last_login_check():
    users = User.objects.filter(is_active=True)
    current_date = now()
    for user in users:
        if user.last_login is None:
            user.last_login = user.date_joined
            user.save()
        if current_date - user.last_login > timedelta(days=30):
            user.is_active = False
            user.save()
