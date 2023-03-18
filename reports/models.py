from django.db import models
from slugify import slugify

from account.models import User


class Reports(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    programm = models.CharField(max_length=3)
    body = models.TextField(blank=True, unique=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=20, primary_key=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.body)
        return super().save()

    def __str__(self) -> str:
        return f'{self.user} - {self.programm}'
    
    
class ReportImage(models.Model):
    report = models.ForeignKey(Reports, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='reports_photo/', blank=True)
