from django.conf import settings
from django.db import models

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )
    preview = models.ImageField(
        upload_to="materials/courses",
        verbose_name="Превью курса",
        help_text="Добавьте превью для курса",
        **NULLABLE
    )
    description = models.TextField(
        verbose_name="Описание курса", help_text="Опишите курс", **NULLABLE
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец курса",
        **NULLABLE,
        help_text="Укажите владельца курса"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )
    description = models.TextField(
        verbose_name="Описание урока", help_text="Опишите урок", **NULLABLE
    )
    preview = models.ImageField(
        upload_to="materials/lessons",
        verbose_name="Превью урока",
        help_text="Добавьте превью для урока",
        **NULLABLE
    )
    video_url = models.URLField(
        verbose_name="Ссылка на видео",
        help_text="Добавьте ссылку на видео для урока",
        **NULLABLE
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец урока",
        **NULLABLE,
        help_text="Укажите владельца урока"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
