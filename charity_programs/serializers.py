from rest_framework import serializers

from . models import Program


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
    
class ProgramListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'
    

    
    



    