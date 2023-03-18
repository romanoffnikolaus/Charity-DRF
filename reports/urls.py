from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings

from . import views


router = DefaultRouter()
router.register('reports', views.ReportView)


urlpatterns = [
    path('', include(router.urls))
]

