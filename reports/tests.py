# from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
# from account.models import User
# from .models import ReportImage, Reports
# from django.core.files import File


# class UserTest(APITestCase):
    
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.user = User.objects.create_user(
#             email='pimp@gmail.com',
#             username='username',
#             first_name='name',
#             last_name='last_name',
#             password='pimp',
#             is_active=True
#         )

#         self.reports = [
#             Reports(user=self.user, programm='top', body='test body'),
#             Reports(user=self.user, programm='top', body='test body 2')
#         ]
#         Reports.objects.bulk_create(self.reports)

#         img = File(open('test_image/Снимок экрана от 2023-01-21 20-25-11.png', 'rb'))
#         report_images = [
#             ReportImage(report=self.reports[0], image=img),
#             ReportImage(report=self.reports[1], image=img)
#         ]
#         ReportImage.objects.bulk_create(report_images)
    
