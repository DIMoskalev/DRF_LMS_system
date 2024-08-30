from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscribe
from materials.paginators import MaterialsPaginator
from materials.serializers import CourseSerializer, LessonSerializer, SubscribeSerializer
from users.permissions import IsModer, IsOwner


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description="Создание курса"
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="Список курсов"
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_description="Подробная информация о курсе"
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_description="Изменение курса"
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_description="Удаление курса"
))
class CourseViewSet(ModelViewSet):
    """ Вьюсет для модели курсов """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = MaterialsPaginator

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (IsOwner | ~IsModer,)
        return super().get_permissions()


class LessonCreateAPIView(CreateAPIView):
    """ Создание урока """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModer, IsAuthenticated,)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(ListAPIView):
    """ Список уроков """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner | ~IsModer)
    pagination_class = MaterialsPaginator


class LessonRetrieveAPIView(RetrieveAPIView):
    """ Просмотр урока """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner,)


class LessonUpdateAPIView(UpdateAPIView):
    """ Изменение урока """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner,)


class LessonDestroyAPIView(DestroyAPIView):
    """ Удаление урока """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner,)


class SubscribeAPIView(APIView):
    """ Добавление и удаление подписки """
    serializer_class = SubscribeSerializer
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_description="Добавление и удаление подписки на курс",
        request_body=SubscribeSerializer(many=True),
        responses={
            200: "Успешное добавление или удаление подписки",
            404: "Курс для подписки не найден",
        },
    )
    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Subscribe.objects.all().filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
            return Response({"message": message})
        else:
            message = "Подписка добавлена"
        return Response({"message": message})

    @swagger_auto_schema(
        operation_description="Список подписок пользователя",
        responses={
            200: "Список подписок пользователя",
        },
    )
    def get(self, *args, **kwargs):
        user = self.request.user
        if user.is_staff:
            subscribe = Subscribe.objects.all()
        else:
            subscribe = Subscribe.objects.filter(user=user)
        serializer = SubscribeSerializer(subscribe, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
