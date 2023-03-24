from django.urls import path

from . import views


urlpatterns = [
    path('donations/', views.DonationListView.as_view()),
    path('payment_process/', views.payment_process, name='payment_process'),
    path('payment_done/', views.payment_done, name='payment_done'),
    path('payment_cancelled/', views.payment_cancelled, name='payment_cancelled'),
]
