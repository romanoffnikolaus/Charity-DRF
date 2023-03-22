from rest_framework import serializers

from .models import ReportRating, ProgramRating, ProgramComment


class ProgramRatingSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(required=True)

    class Meta:
        model = ProgramRating
        fields = 'rating',

    def validate_rating(self, rating):
        if 1 <= rating <= 5:
            return rating
        raise serializers.ValidationError('Invalid number, should be in range 1, 5')

class ProgramCommentSerializer(serializers.ModelSerializer):
    comment = serializers.CharField()

    class Meta:
        model = ProgramComment
        fields = 'comment',


class ReportRatingSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(required=True)

    class Meta:
        model = ReportRating
        fields = 'rating',

    def validate_rating(self, rating):
        if 1 <= rating <= 5:
            return rating
        raise serializers.ValidationError('Invalid number, should be in range 1, 5')
