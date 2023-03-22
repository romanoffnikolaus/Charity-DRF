from rest_framework import serializers
from django.db.models import Avg

from .models import Reports, ReportImage


class ReportImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportImage
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    images = ReportImageSerializer(many=True, read_only=True)

    class Meta:
        model = Reports
        fields = '__all__'
        extra_kwargs = {
            'body': {'required': True}
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['rating'] = instance.report_ratings.aggregate(Avg('rating'))['rating__avg']
        return representation
