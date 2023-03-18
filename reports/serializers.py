from rest_framework import serializers
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