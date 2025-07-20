from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
class User(AbstractUser):
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class Assignment(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    file = models.FileField(upload_to='submissions/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
