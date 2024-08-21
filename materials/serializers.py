from rest_framework.fields import SerializerMethodField
from rest_framework import serializers

from materials.models import Course, Lesson, Subscribe
from materials.validators import validate_video_url


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[validate_video_url], required=False)

    class Meta:
        model = Lesson
        fields = ("id", "title", "description", "preview", "video_url", "course", "owner",)


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = SerializerMethodField()
    lessons = LessonSerializer(many=True, source='lesson_set', required=False)
    subscribe = serializers.SerializerMethodField(read_only=True)

    def get_count_lessons(self, obj):
        return obj.lesson_set.count()

    def get_subscribe(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscribe.objects.filter(user=request.user, course=obj).exists()
        return False

    class Meta:
        model = Course
        fields = "__all__"


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = '__all__'

    def to_representation(self, obj):
        request = self.context.get('request')
        if request:
            user = request.user
            if user.is_staff or obj.user == user:
                return super().to_representation(obj)
            return {'message': 'Недостаточно прав для просмотра информации о подписках.'}
        return super().to_representation(obj)
