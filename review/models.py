from django.db import models

from charity_programs.models import Program
from reports.models import Reports
from account.models import User


class ProgramRating(models.Model):
    program = models.ForeignKey(
        Program, on_delete=models.CASCADE, related_name='program_ratings')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_program_ratings')
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{str(self.rating)}'


class ProgramComment(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='program_comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    comment = models.TextField()
    is_liked = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} comment on: {self.program}'


class ReportRating(models.Model):
    report = models.ForeignKey(
        Reports, on_delete=models.CASCADE, related_name='report_ratings')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_report_ratings')
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{str(self.rating)}'
