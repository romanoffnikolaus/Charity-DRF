from rest_framework import serializers
from django.contrib.auth import get_user_model

from . import models


User = get_user_model()

class DonationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.id')
    charity_program = serializers.ReadOnlyField(source = 'charity_program.slug')
    
    class Meta:
        model = models.Donation
        fields = '__all__'