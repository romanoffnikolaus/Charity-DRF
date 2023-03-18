from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('charity_programs', views.ProgramsViewSet)

urlpatterns = [
    path('', include(router.urls))
]