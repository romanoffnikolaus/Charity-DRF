from django.db import models
from slugify import slugify

from account.models import User
from charity_programs.models import Program


class Reports(models.Model):
    title = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='report')
    body = models.TextField(blank=True, unique=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(primary_key=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save()

    def __str__(self) -> str:
        return f'{self.user} - {self.program}'
    
    
class ReportImage(models.Model):
    report = models.ForeignKey(Reports, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='reports_photo/', blank=True)
