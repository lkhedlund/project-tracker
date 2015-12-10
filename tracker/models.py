from django.db import models
from django.utils import timezone

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    total_count = models.IntegerField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    total_count = models.IntegerField()
    user_id = models.ForeignKey('auth.User')

class Count(models.Model):
    count_update = models.IntegerField()
    created_date = models.DateField(default=timezone.now)
    project_id = models.ForeignKey(Project)
