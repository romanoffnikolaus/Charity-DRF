from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from .models import Reports, ReportImage
from .serializers import ReportSerializer, ReportImageSerializer


class ReportView(ModelViewSet):
    queryset = Reports.objects.all()
    serializer_class = ReportSerializer
    parser_classes = [MultiPartParser]

    def create(self, request, *args, **kwargs):
        images = request.FILES.getlist('images')
        data = request.data.copy()
        data.pop('images')
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
        print(instance)
        images_serializer = ReportImageSerializer(report_images, many=True)
        response_data = {**serializer.data,'images':images_serializer.data,}
        return Response(response_data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        images = request.FILES.getlist('images')
        data = request.data.copy()
        data.pop('images')
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        instance.reportimage_set.all().delete()
        for image in images:
            ReportImage.objects.create(report=instance, image=image)
        response_data = serializer.data
        report_images = instance.reportimage_set.all()
        images_serializer = ReportImageSerializer(report_images, many=True)
        response_data['images'] = images_serializer.data
        return Response(response_data)