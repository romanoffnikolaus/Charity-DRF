from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
import django_filters
from rest_framework import filters

from . import models
from . import serializers
from . import permissions as p


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
