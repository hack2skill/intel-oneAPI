from django.db import models

class Question(models.Model):
    
    text = models.CharField(max_length=255)

    option1 = models.CharField(max_length=255, default='Default Option 1')

    option2 = models.CharField(max_length=255, default='Default Option 2')

    option3 = models.CharField(max_length=255, default='Default Option 3')

    option4 = models.CharField(max_length=255, default='Default Option 4')

    correct_answer = models.CharField(max_length=255, default='Nothing')

