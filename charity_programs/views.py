from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
import django_filters

from . import models
from . import serializers
from . import permissions as p
from review.serializers import ProgramCommentSerializer, ProgramRatingSerializer
from review.models import ProgramRating, ProgramComment


class ProgramsViewSet(ModelViewSet):
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['title']
    ordering = ['title']
    queryset = models.Program.objects.all()
    serializer_class = serializers.ProgramSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [p.permissions.AllowAny]
        elif self.action in ['update', 'destroy', 'partial_update']:
            self.permission_classes = [p.IsCreatorPermission, p.permissions.IsAuthenticated]
        return super().get_permissions()

    @action(methods=['POST'], detail=True)
    def rate(self, request, pk=None):
        program = self.get_object()
        user = request.user
        serializer = ProgramRatingSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                rated_program = ProgramRating.objects.get(program=program, user=user)
            except ProgramRating.DoesNotExist:
                rating = serializer.validated_data.get('rating')
                ProgramRating.objects.create(program=program, user=user, rating=rating)
            else:
                rating = serializer.validated_data.get('rating')
                rated_program.rating = rating
                rated_program.save()
        return Response(serializer.data)

    @action(methods=['POST'], detail=True)
    def comment(self, request, pk=None):
        program = self.get_object()
        user = request.user
        serializer = ProgramCommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                commented_program = ProgramComment.objects.get(program=program, user=user)
            except ProgramComment.DoesNotExist:
                comment = serializer.validated_data.get('comment')
                ProgramComment.objects.create(program=program, user=user, comment=comment)
            else:
                comment = serializer.validated_data.get('comment')
                commented_program.comment = comment
                commented_program.save()
        return Response(serializer.data)
