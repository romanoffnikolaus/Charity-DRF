from django.urls import path

from . import views


urlpatterns = [
    path('your_donations/', views.DonationListView.as_view()),
    path('payment_process/', views.payment_process, name='payment_process'),
    path('payment_done/', views.payment_done, name='payment_done'),
    path('payment_cancelled/', views.payment_cancelled, name='payment_cancelled'),
    path('all_donations/', views.AllDonationListView.as_view(), name='all_dontaions')
]

