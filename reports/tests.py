from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from django.core.files import File
from collections import OrderedDict

from account.models import User
from .models import ReportImage, Reports
from charity_programs.models import Program
from program_categories.models import Category
from . import views

class UserTest(APITestCase):
    
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            email='pimp@gmail.com',
            username='username',
            first_name='name',
            last_name='last_name',
            password='pimp',
            is_active=True
        )
        self.category = Category.objects.create(title='test category')
        self.program = Program.objects.create(
            user=self.user,
            title='test program',
            category=self.category
        )

        self.reports = Reports.objects.create(
            title='test report',
            user=self.user,
            program=self.program,
            body='test body'
        )

        img = File(open('test_image/Снимок экрана от 2023-01-21 20-25-11.png', 'rb'))
        self.report_image = ReportImage.objects.create(
            report=self.reports,
            image=img
        )


    def test_list(self):
        request = self.factory.get('reports/')
        view = views.ReportView.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        assert type(response.data) == OrderedDict
    
    def test_delete(self):
        user = User.objects.all()[0]
        slug = Reports.objects.all()[0].slug
        request = self.factory.delete(f'reports/{slug}')
        force_authenticate(request, user=user)
        view = views.ReportView.as_view({'delete':'destroy'})
        response = view(request, pk=slug)
        assert response.status_code == 204
    
    def test_create(self):
        user = User.objects.all()[0]
        data = {
        'title': 'Чудо-нож',
        'program': self.program.slug,
        'body': 'test_body',
        'user': user.email,
        'images': [self.report_image.image]
        }
        request = self.factory.post('reports/', data, format='multipart')
        force_authenticate(request, user=user)
        view = views.ReportView.as_view({'post':'create'})
        response = view(request)
        assert response.status_code == 201
        assert response.data['title'] == data['title']
    
    def test_update(self):
        user = User.objects.all()[0]
        slug = Reports.objects.all()[0].slug
        data = {
        'program': self.program.slug,
        'body': 'test_body',
        'user': user.email,
        'images': [self.report_image.image]
        }
        request = self.factory.patch(f'reports/{slug}', data, format='multipart')
        force_authenticate(request, user=user)
        view = views.ReportView.as_view({'patch':'partial_update'})
        response = view(request, pk=slug)
        assert response.status_code == 200
        assert response.data['body'] == data['body']
    
