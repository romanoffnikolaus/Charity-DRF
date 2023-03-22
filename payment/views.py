from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions

from . models import Donation
from . import serializers


class DonationListView(generics.ListAPIView):
    queryset = Donation.objects.all()
    serializer_class = serializers.DonationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        self.queryset = Donation.objects.filter(user=request.user)
        return super().list(request, *args, **kwargs)
    
