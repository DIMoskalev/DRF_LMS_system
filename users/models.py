from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    phone = models.CharField(
        max_length=35,
        verbose_name="Телефон",
        help_text="Укажите номер телефона",
        **NULLABLE
    )
    city = models.CharField(
        max_length=50, verbose_name="Город", help_text="Укажите свой город", **NULLABLE
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="Аватар",
        help_text="Загрузите аватар",
        **NULLABLE
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payments(models.Model):

    CASH = 'CASH'
    ONLINE = 'ONLINE'
    PAYMENT_METHODS = (
        (CASH, 'Наличными'),
        (ONLINE, 'Онлайн')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Оплаченный курс', **NULLABLE)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Оплаченный урок', **NULLABLE)
    payment_amount = models.IntegerField(verbose_name='Сумма оплаты')
    payment_method = models.CharField(max_length=35, verbose_name='Метод оплаты', choices=PAYMENT_METHODS)

    def __str__(self):
        if self.paid_course:
            return f'{self.user} - {self.paid_course} руб.'
        else:
            return f'{self.user} - {self.paid_lesson} руб.'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
