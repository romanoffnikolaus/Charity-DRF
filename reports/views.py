from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action

from .models import Reports, ReportImage
from .serializers import ReportSerializer, ReportImageSerializer
from .permissions import IsProgramOwnerOrReadOnly, IsOwnerOrReadOnly
from review.models import ReportRating
from review.serializers import ReportRatingSerializer


class PermissionsMixin():
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permissions = [AllowAny]
        elif self.action in ['create']:
            permissions = [IsProgramOwnerOrReadOnly]
        elif self.action in ['update', 'partial_update', 'destroy', ]:
            permissions = [IsOwnerOrReadOnly]
        else:
            permissions = [AllowAny]
        return [permission() for permission in permissions]


class ReportView(PermissionsMixin, ModelViewSet):
    queryset = Reports.objects.all()
    serializer_class = ReportSerializer
    parser_classes = [MultiPartParser]

    def create(self, request, *args, **kwargs):
        images = request.FILES.getlist('images')
        data = request.data.copy()
        data.pop('images',None)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        report = serializer.save(user=self.request.user)
        for image in images:
            ReportImage.objects.create(report=report, image=image)
        return Response(serializer.data, status=201)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        report_images = instance.reportimage_set.all()
        images_serializer = ReportImageSerializer(report_images, many=True)
        response_data = {**serializer.data,'images':images_serializer.data,}
        return Response(response_data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        images = request.FILES.getlist('images')
        data = request.data.copy()
        data.pop('images', None)
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if images:
            instance.reportimage_set.all().delete()
            for image in images:
                ReportImage.objects.create(report=instance, image=image)

        response_data = serializer.data
        report_images = instance.reportimage_set.all()
        images_serializer = ReportImageSerializer(report_images, many=True)
        response_data['images'] = images_serializer.data
        return Response(response_data)

    @action(methods=['POST'], detail=True)
    def rate(self, request, pk=None):
        report = self.get_object()
        user = request.user
        serializer = ReportRatingSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                rated_report = ReportRating.objects.get(report=report, user=user)
            except ReportRating.DoesNotExist:
                rating = serializer.validated_data.get('rating')
                ReportRating.objects.create(
                    report=report, user=user, rating=rating)
            else:
                rating = serializer.validated_data.get('rating')
                rated_report.rating = rating
                rated_report.save()
        return Response(serializer.data)
