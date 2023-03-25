from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
import django_filters
from django.shortcuts import redirect
from django.urls import reverse 
from drf_yasg.utils import swagger_auto_schema

from . import models
from . import serializers
from . import permissions as p
from payment.serializers import DonationSerializer
from review.serializers import ProgramCommentSerializer, ProgramRatingSerializer
from review.models import ProgramRating, ProgramComment
from payment.models import Donation

class ProgramsViewSet(ModelViewSet):
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter]
    search_fields = ['title', 'user__user_type']
    filterset_fields = ['user__user_type', 'category', 'region']
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
    
    @swagger_auto_schema(request_body=DonationSerializer)
    @action(methods = ['POST'], detail=True)
    def donate(self, request, pk):
        program = self.get_object()
        user = request.user
        amount = request.data['amount']
        donation =Donation.objects.create(charity_prigram=program, user=user, amount=amount)
        request.session['donation_id'] = donation.id
        return redirect('payment_process')
