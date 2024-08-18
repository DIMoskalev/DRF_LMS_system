from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ("id", "title", "description", "preview", "video_url", "course", "owner",)


class CourseSerializer(ModelSerializer):
    count_lessons = SerializerMethodField()
    lessons = LessonSerializer(many=True, source='lesson_set', required=False)

    def get_count_lessons(self, obj):
        return obj.lesson_set.count()

    class Meta:
        model = Course
        fields = "__all__"
