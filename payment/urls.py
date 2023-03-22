from django.urls import path

from . import views


urlpatterns = [
    path('donations/', views.DonationListView.as_view())
]

