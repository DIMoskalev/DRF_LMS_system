from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig
from materials.views import (CourseViewSet, LessonCreateAPIView,
                             LessonDestroyAPIView, LessonListAPIView,
                             LessonRetrieveAPIView, LessonUpdateAPIView, SubscribeAPIView)

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register("", CourseViewSet, basename="courses")

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name="lessons-list"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lesson-create"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson-retrieve"),
    path("lessons/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lesson-update"),
    path("lessons/delete/<int:pk>/", LessonDestroyAPIView.as_view(), name="lesson-delete"),
    path("subscribe/", SubscribeAPIView.as_view(), name="subscribe"),
] + router.urls
