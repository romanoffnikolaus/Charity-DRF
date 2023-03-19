from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
import django_filters
from rest_framework.pagination import PageNumberPagination

from . import serializers
from .permissions import IsOwnerOrReadOnly


User = get_user_model()


class PermissionMixin:
    permission_classes = [IsAuthenticated]


class RegistrationView(generics.CreateAPIView):
    serializer_class = serializers.RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ActivationView(APIView):
    def get(self, request, email, activation_code):
        user = User.objects.filter(
            email=email,
            activation_code=activation_code).first()
        if not user:
            return Response('User is not found', status=400)
        user.activation_code = ''
        user.is_active = True
        user.save()
        return Response('Activated', status=200)


class ChangePasswordView(PermissionMixin, APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=serializers.ChangePasswordSerializer)
    def post(self, request):
        serializer = serializers.ChangePasswordSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            message = 'Successful'
            return Response(serializer.validated_data)
        else:
            message = 'Uncorrecct password'
            return Response(message)
        


class ForgotPasswordView(PermissionMixin, APIView):
    @swagger_auto_schema(request_body=serializers.ForgotPasswordSerializer)
    def post(self, request):
        serializer = serializers.ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_verification_email()
            return Response('You will receive a link to reset your password.')


class ForgotPasswordCompleteView(PermissionMixin, APIView):
    @swagger_auto_schema(request_body=serializers.ForgotPasswordCompleteSerializer)
    def post(self, request):
        serializer = serializers.ForgotPasswordCompleteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response(serializer.validated_data)


class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        username = request.data.get('username')
        user = User.objects.get(username=username)
        user_data = {'id': user.id}
        new_data = list(user_data.items())
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        serializer.validated_data.update(new_data)
        return Response(serializer.validated_data, status=200)


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = []

    def update(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        user = User.objects.get(username = request.user.username)
        print(user.verified_account)
        if 'user_type' in request.data.keys():
            if request.data['user_type'] != 'Default user' and request.user.user_type == 'Default user':
                user.verified_account = False
            if request.data['user_type'] == 'Default user' and request.user.user_type != 'Default user':
                user.verified_account = True
        user.save()
        return super().update(request, *args, **kwargs)


class UserListPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.ProfileSerializer
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter]
    ordering_fields = ['date_joined']
    filterset_fields = ['verified_account', 'user_type']
    search_fields = ['date_joined']
    pagination_class = UserListPagination
