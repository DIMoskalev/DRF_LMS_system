from rest_framework.serializers import ModelSerializer

from users.models import User, Payments


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone")


class PaymentsSerializer(ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"
