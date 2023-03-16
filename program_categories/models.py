from django.db import models
from slugify import slugify


class Category(models.Model):
    title = models.CharField(max_length=150, blank=False, unique=True)
    slug = models.SlugField(max_length=150, blank=True, unique=True, primary_key=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
            self.slug = slugify(self.title)
            return super().save(*args, **kwargs)
        
