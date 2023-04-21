import datetime

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import filters
from rest_framework.decorators import api_view
import django_filters
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.shortcuts import redirect

from . import serializers
from .permissions import IsOwnerOrReadOnly
from .models import User
from payment.models import Donation
from payment.serializers import DonationSerializer



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
        username = request.data.get('email')
        try:
            user = User.objects.get(email=username)
        except Exception:
            return  Response({'error':'Invalid email'}, status=401)
        user_data = {'id': user.id}
        new_data = list(user_data.items())
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        serializer.validated_data.update(new_data)
        return Response(serializer.validated_data, status=200)


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def update(self, request, *args, **kwargs):
        user = User.objects.get(username = request.user.username)
        print(user.verified_account)
        if 'user_type' in request.data.keys():
            if request.data['user_type'] != 'default_user' and request.user.user_type == 'default_user':
                user.verified_account = False
            if request.data['user_type'] == 'default_user' and request.user.user_type != 'default_user':
                user.verified_account = True
        user.save()
        return super().update(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        self.permission_classes = [AllowAny]
        return super().retrieve(request, *args, **kwargs)
    


class DonateToFundView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=DonationSerializer)
    def post(self, request, pk= None):
        fund = User.objects.get(id=pk)
        user = request.user
        amount = request.data['amount']
        donation =Donation.objects.create(fund=fund, user=user, amount=amount)
        request.session['donation_id'] = donation.id
        return redirect('payment_process')


class UserListPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class HelpersFundsListView(generics.ListAPIView):
    queryset = User.objects.filter(Q(user_type='fund') | Q(user_type='user_helper'))
    serializer_class = serializers.ProfileSerializer
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter]
    ordering_fields = ['date_joined', 'user_type', 'region', 'category', 'username']
    filterset_fields = ['verified_account', 'user_type', 'region', 'category', 'username']
    search_fields = ['date_joined', 'region', 'category__title', 'username']
    pagination_class = UserListPagination


class UsersListView(generics.ListAPIView):
    queryset = User.objects.filter(user_type='default_user')
    serializer_class = serializers.ProfileSerializer
    filter_backends = [
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter]
    ordering_fields = ['date_joined']
    filterset_fields = ['verified_account']
    search_fields = ['date_joined']
    pagination_class = UserListPagination


class TopDonaters(generics.ListAPIView):
    queryset = User.objects.filter(user_type='default_user')
    serializer_class = serializers.ProfileSerializer
    

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            top_number = 1
            sorted_top = list(sorted(serializer.data, key=lambda d : d['all_donations'], reverse=True))
            for dict in sorted_top:
                dict['top_id'] = top_number
                top_number += 1
            return self.get_paginated_response(sorted_top)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class MainPageView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        all_sum = sum(map(lambda d: d.amount,Donation.objects.all()))
        today_sum = sum(map(lambda d: d.amount, Donation.objects.filter(donation_date__contains=datetime.date.today())))
        timedelta = datetime.timedelta(days=30)
        last_30_days = datetime.date.today() - timedelta
        print(last_30_days)
        last_30_days_donations_sum = sum(map(lambda d: d.amount, Donation.objects.filter(donation_date__gte=last_30_days)))
        data = {'all_donations': all_sum, 'today_donations':today_sum, 'last_30_days_donations':last_30_days_donations_sum}
        return Response(data)

