
# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# Example model stored in secondary DB for import sync
class TaskSecondary(models.Model):
    class Meta:
        app_label = 'secondary'  # send this model to secondary DB
        db_table = 'secondary_tasksecondary'

    # replicate fields from Task as needed
    user_id = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10)
    imported_at = models.DateTimeField(auto_now_add=True)
