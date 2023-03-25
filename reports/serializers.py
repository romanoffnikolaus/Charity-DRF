from rest_framework import serializers
from django.db.models import Avg

from .models import Reports, ReportImage


class ReportImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ReportImage
        fields = ('id', 'report', 'image', 'image_url')

    def get_image_url(self, obj): #Изменить URL перед деплоем. Это костыль.
        if obj.image:
            return f'https://savethedayteam.com/media/{obj.image.name}'
        return None
    
    
class ReportSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
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
