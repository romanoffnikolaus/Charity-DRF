from rest_framework import serializers
from django.db.models import Avg

from .models import Program
from review.serializers import ProgramCommentSerializer
from review.models import ProgramComment


class ProgramSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Program
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user

        print(validated_data)
        program = Program.objects.create(user=user, **validated_data)
        return program

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['rating'] = instance.program_ratings.aggregate(Avg('rating'))[
            'rating__avg']
        representation['comments'] = ProgramCommentSerializer(
            ProgramComment.objects.filter(program=instance.pk),
            many=True).data
        return representation
