from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Lesson, Course, Subscribe
from users.models import User


class LessonTestCaseOwner(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(title="Вязание", description="Курсы вязания крестиком для начинающих",
                                            owner=self.user)
        self.lesson = Lesson.objects.create(title="Урок 1", description="Ознакомительный(вводный) урок",
                                            course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("materials:lesson-retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data["title"], self.lesson.title
        )

    def test_lesson_create(self):
        url = reverse("materials:lesson-create")
        data = {
            "title": "Урок 2",
            "description": "Подбор хороших материалов для вязания",
            "course": self.course.pk,
            "owner": self.user.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_lesson_update(self):
        url = reverse("materials:lesson-update", args=(self.lesson.pk,))
        data = {
            "title": "Новая версия 1го урока",
        }
        response = self.client.patch(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            Lesson.objects.get(pk=self.lesson.pk).title, "Новая версия 1го урока"
        )

    def test_lesson_delete(self):
        url = reverse("materials:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lessons_list(self):
        url = reverse("materials:lessons-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "title": self.lesson.title,
                    "description": self.lesson.description,
                    "preview": None,
                    "video_url": None,
                    "course": self.lesson.course.pk,
                    "owner": self.lesson.owner.pk
                },
            ]
        }
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            len(data), 4
        )
        self.assertEqual(
            data, result
        )


class LessonTestCaseNotOwner(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(title="Вязание", description="Курсы вязания крестиком для начинающих", )
        self.lesson = Lesson.objects.create(title="Урок 1", description="Ознакомительный(вводный) урок",
                                            course=self.course, )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("materials:lesson-retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )

    def test_lesson_create(self):
        url = reverse("materials:lesson-create")
        data = {
            "title": "Урок 2",
            "description": "Подбор хороших материалов для вязания",
            "course": self.course.pk,
            "owner": self.user.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_lesson_update(self):
        url = reverse("materials:lesson-update", args=(self.lesson.pk,))
        data = {
            "title": "Новая версия 1го урока",
        }
        response = self.client.patch(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )
        self.assertEqual(
            Lesson.objects.get(pk=self.lesson.pk).title, "Урок 1"
        )

    def test_lesson_delete(self):
        url = reverse("materials:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )
        self.assertEqual(
            Lesson.objects.all().count(), 1
        )

    def test_lessons_list(self):
        url = reverse("materials:lessons-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "title": self.lesson.title,
                    "description": self.lesson.description,
                    "preview": None,
                    "video_url": None,
                    "course": self.lesson.course.pk,
                    "owner": None
                },
            ]
        }
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            len(data), 4
        )
        self.assertEqual(
            data, result
        )


class LessonTestCaseNotAuthenticate(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(title="Вязание", description="Курсы вязания крестиком для начинающих", )
        self.lesson = Lesson.objects.create(title="Урок 1", description="Ознакомительный(вводный) урок",
                                            course=self.course, )

    def test_lesson_retrieve(self):
        url = reverse("materials:lesson-retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)

        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )

    def test_lesson_create(self):
        url = reverse("materials:lesson-create")
        data = {
            "title": "Урок 2",
            "description": "Подбор хороших материалов для вязания",
            "course": self.course.pk,
            "owner": self.user.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 1
        )

    def test_lesson_update(self):
        url = reverse("materials:lesson-update", args=(self.lesson.pk,))
        data = {
            "title": "Новая версия 1го урока",
        }
        response = self.client.patch(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )
        self.assertEqual(
            Lesson.objects.get(pk=self.lesson.pk).title, "Урок 1"
        )

    def test_lesson_delete(self):
        url = reverse("materials:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 1
        )

    def test_lessons_list(self):
        url = reverse("materials:lessons-list")
        response = self.client.get(url)

        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )


class SubscribeTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(title="Вязание", description="Курсы вязания крестиком для начинающих",
                                            owner=self.user)
        self.lesson = Lesson.objects.create(title="Урок 1", description="Ознакомительный(вводный) урок",
                                            course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscribe_create(self):
        url = reverse("materials:subscribe")
        data = {
            "course": self.course.pk,
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            response.data.get("message"), "Подписка добавлена"
        )

    def test_subscribe_delete(self):
        url = reverse("materials:subscribe")
        Subscribe.objects.create(user=self.user, course=self.course)
        data = {
            "course": self.course.pk,
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            response.data.get("message"), "Подписка удалена"
        )


class SubscribeTestCaseNotAuthenticate(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(title="Вязание", description="Курсы вязания крестиком для начинающих",
                                            owner=self.user)
        self.lesson = Lesson.objects.create(title="Урок 1", description="Ознакомительный(вводный) урок",
                                            course=self.course, owner=self.user)

    def test_subscribe_create(self):
        url = reverse("materials:subscribe")
        data = {
            "course": self.course.pk,
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )

    def test_subscribe_delete(self):
        url = reverse("materials:subscribe")
        Subscribe.objects.create(user=self.user, course=self.course)
        data = {
            "course": self.course.pk,
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )
