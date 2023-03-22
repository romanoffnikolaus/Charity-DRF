from django.db import models
from django.contrib.auth import get_user_model

from charity_programs.models import Program


User = get_user_model()

class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='donations')
    charity_prigram = models.ForeignKey(Program, on_delete=models.RESTRICT, related_name='donations')
    amount = models.FloatField()
    donation_date =models.DateTimeField(auto_now_add=True)

