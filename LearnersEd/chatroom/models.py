from django.db import models
from django.utils import timezone
from login_register.models import Student

class ChatMessage(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.message
