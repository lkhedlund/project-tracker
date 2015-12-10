from django.db import models
from django.utils import timezone

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    total_count = models.IntegerField()
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    user_id = models.ForeignKey('auth.User')

    def __str__(self):
        return self.title

class Count(models.Model):
    count_update = models.IntegerField()
    created_date = models.DateField(default=timezone.now)
    project_id = models.ForeignKey(Project)

    def __str__(self):
        return self.count_update
