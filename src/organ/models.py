from django.conf import settings
from django.db import models
import random
import string
from django.utils import timezone
from datetime import timedelta


class EmailVerification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    @classmethod
    def generate_code(cls):
        return ''.join(random.choices(string.digits, k=6))

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(hours=24)

    def __str__(self):
        return f"{self.user.email} - {self.code}"


class TaskCategory(models.Model):
    CATEGORY_CHOICES = [
        ('important_urgent', 'Важное срочное'),
        ('important_not_urgent', 'Важное не срочное'),
        ('not_important_urgent', 'Не важное срочное'),
        ('not_important_not_urgent', 'Не важное не срочное'),
    ]
    
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)
    
    def __str__(self):
        return self.get_name_display()


class Tasks(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=25)
    descriptionn = models.CharField(blank=True, max_length=255)
    statuss = models.BooleanField(default=False)
    time_create = models.DateTimeField(auto_now_add=True)
    time_finish = models.DateTimeField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    category = models.ForeignKey(
        TaskCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Категория"
    )

    def __str__(self):
        return self.title


class Subtasks(models.Model):
    task = models.ForeignKey(
        Tasks,
        on_delete=models.CASCADE
    )
    text = models.CharField(max_length=30)
    is_finished = models.BooleanField(default=False)
