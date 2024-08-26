from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.models import User, Payments
from users.serializers import UserSerializer, PaymentsSerializer
from users.services import create_stripe_product, create_stripe_price, create_stripe_session


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description="Создание пользователя"
))
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="Список пользователей"
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_description="Подробная информация о пользователе"
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_description="Изменение информации о пользователе"
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_description="Удаление пользователя"
))
class UserViewSet(ModelViewSet):
    """ Вьюсет для модели пользователя """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentsListAPIView(ListAPIView):
    """ Список платежей """
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering_fields = ('date',)
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')


class PaymentsCreateAPIView(CreateAPIView):
    """ Список платежей """
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        if payment.paid_course:
            current_product = payment.paid_course
        else:
            current_product = payment.paid_lesson
        product_id = create_stripe_product(current_product)
        price_id = create_stripe_price(current_product, product_id)
        session_id, payment_link = create_stripe_session(price_id)
        payment.session_id = session_id
        payment.link = payment_link
        payment.payment_amount = current_product.price
        payment.save()
