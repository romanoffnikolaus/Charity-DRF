from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import filters
import django_filters 

from . import models
from . import serializers


class CategoryView(generics.ListAPIView):
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['title']
    ordering = ['title']
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    
            
