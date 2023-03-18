from django.db import models
from django.contrib.auth import get_user_model
from slugify import slugify
from program_categories.models import Category

User = get_user_model()

class Program(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='charity_programs')
    title = models.CharField(max_length=150, unique=True, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='charity_programs')
    slug = models.SlugField(max_length=150, primary_key=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Programs'

    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
