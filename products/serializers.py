from rest_framework import serializers
from .models import Lesson, View, Product


class LessonSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField(source='get_status_display')
    last_viewed = serializers.SerializerMethodField()


class Meta:
    model = Lesson
    fields = ['id', 'title', 'video_link', 'duration', 'status', 'last_viewed']

    def get_last_viewed(self, obj):
        user = self.context['request'].user

        try:
            last_view = obj.view_set.filter(user=user).latest('watched_time')
            return last_view.watched_time
        except View.DoesNotExist:
            return None


class ProductStatisticSerializer(serializers.ModelSerializer):
    num_views = serializers.IntegerField(read_only=True)
    total_time = serializers.IntegerField(read_only=True)
    num_users = serializers.IntegerField(read_only=True)
    acquisition_percentage = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)


class Meta:
    model = Product
    fields = ['id', 'name', 'num_views', 'total_time', 'num_users', 'acquisition_percentage']