from datetime import timedelta, datetime

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from pytz import timezone

from materials.models import Course, Subscribe
from users.models import User


@shared_task
def course_update_notification(course_pk):
    course = Course.objects.get(pk=course_pk)
    subscribe = Subscribe.objects.filter(course=course.pk)
    for sub in subscribe:
        if sub:
            send_mail(
                subject=f'Обновился курс {course.title}',
                message=f'Курс {course.title}, на который вы подписаны был обновлен',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[sub.user.email],
            )
