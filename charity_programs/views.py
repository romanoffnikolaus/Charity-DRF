from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
import django_filters
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.decorators import action

from . import models
from . import serializers
from . import permissions as p
from payment.models import Donation


class ProgramsViewSet(ModelViewSet):
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter]
    search_fields = ['title', 'user__user_type']
    # filterset_fields = 'user__user_type'
    ordering_fields = ['title', 'created_at']
    
    ordering = ['title']
    queryset = models.Program.objects.all()
    serializer_class = serializers.ProgramSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1 
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [p.permissions.AllowAny]
        elif self.action in ['update', 'destroy', 'partial_update']:
            self.permission_classes = [p.IsCreatorPermission, p.permissions.IsAuthenticated]
        elif self.action in ['create']:
            self.permission_classes = [p.permissions.IsAuthenticated, p.IsDefaultUserPermission]
        return super().get_permissions()
    
    def get_serializer_class(self):
        if self.action == 'list':
             self.serializer_class = serializers.ProgramListSerializer
        return super().get_serializer_class()
    
    @action(methods = ['POST'], detail=True)
    def donate(self, request, pk):
        program = self.get_object()
        user = request.user
        amount = request.data['amount']
        donation =Donation.objects.create(program=program, user=user, amount=amount)
        donation.save()
        return Response('you are donated succesfully')





    

    
