from rest_framework import serializers
from django.db.models import Avg

from .models import Program
from review.serializers import ProgramCommentSerializer
from review.models import ProgramComment
from payment.models import Donation


class ProgramSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Program
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        program = Program.objects.create(user=user, **validated_data)
        return program

    def validate_donations_goal(self, donation_goal):
        if donation_goal <= 0:
            raise serializers.ValidationError(
                'Goal must be positive number'
            )
        return donation_goal

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['rating'] = instance.program_ratings.aggregate(Avg('rating'))[
            'rating__avg']
        representation['comments'] = ProgramCommentSerializer(
            ProgramComment.objects.filter(program=instance.pk),
            many=True).data
        queryset = Donation.objects.filter(charity_prigram=instance)
        representation['donations_sum'] = sum(list(map(lambda k: k.amount, queryset)))
        return representation
