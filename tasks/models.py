from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients')
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        unique_together = ['user', 'name']  # Same client name can exist for different users

    def __str__(self):
        return self.name

    @property
    def total_tasks(self):
        return self.tasks.count()

    @property
    def completed_tasks(self):
        return self.tasks.filter(is_completed=True).count()

    @property
    def pending_tasks(self):
        return self.tasks.filter(is_completed=False).count()

    @property
    def completion_percentage(self):
        if self.total_tasks == 0:
            return 0
        return round((self.completed_tasks / self.total_tasks) * 100)

    @property
    def remaining_percentage(self):
        return 100 - self.completion_percentage


class Task(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=500)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        checkbox = "☑" if self.is_completed else "□"
        return f"{checkbox} {self.title}"
