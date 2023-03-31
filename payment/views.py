from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from django.conf import settings
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.urls import reverse 

from . models import Donation
from . import serializers


class DonationListView(generics.ListAPIView):
    queryset = Donation.objects.all()
    serializer_class = serializers.DonationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        self.queryset = Donation.objects.filter(user=request.user)
        return super().list(request, *args, **kwargs)
    

class AllDonationListView(generics.ListAPIView):
    queryset = Donation.objects.all()
    serializer_class = serializers.DonationSerializer


@csrf_exempt
def payment_done(request):
    return render (request, 'payment/payment_done.html')


@csrf_exempt
def payment_cancelled(request):
    return render(request, 'payment/payment_cancelled.html')    


@csrf_exempt
def payment_process(request):
    host = request.get_host()
    donation_id = request.session.get('donation_id')
    donation = Donation.objects.get(id=donation_id)

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % Decimal(donation.amount).quantize(
            Decimal('.01')),
        'item_name': 'donation {}'.format(donation.id),
        'invoice': str(donation_id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                        reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                        reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                            reverse('payment_cancelled')),
        }

    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {'donation': donation, 'form': form, 'amount': donation.amount}
    return render(request, 'payment/process_payment.html', context)

