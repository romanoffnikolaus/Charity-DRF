from django.db import models
from django.contrib.auth import get_user_model

from charity_programs.models import Program


User = get_user_model()

class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='donations', blank=True, null=True )
    charity_prigram = models.ForeignKey(Program, on_delete=models.RESTRICT, related_name='donations', blank=True, null=True)
    amount = models.FloatField()
    fund = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='fund_donations', blank=True, null=True )
    donation_date =models.DateTimeField(auto_now_add=True)

