from django.db import models
from django.utils import timezone

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    total_count = models.IntegerField(default=0)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    user_id = models.ForeignKey('auth.User')
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Count(models.Model):
    count_update = models.IntegerField(default=0, null=False)
    created_date = models.DateField(default=timezone.now)
    project = models.ForeignKey('tracker.Project', related_name='counts')

    def __str__(self):
        return str(self.count_update)
