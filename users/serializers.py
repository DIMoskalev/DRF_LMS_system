from rest_framework.serializers import ModelSerializer

from users.models import User, Payments


class PaymentsSerializer(ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"


class UserSerializer(ModelSerializer):
    payments = PaymentsSerializer(many=True, source="payments_set", read_only=True)

    class Meta:
        model = User
        fields = "__all__"
