from django.db import models
from django.conf import settings


class Tasks(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks",
        blank=False
    )
    title = models.CharField(max_length=25, default="Название задачи")
    descriptionn = models.CharField(blank=True, max_length=255, default="Описание задачи")
    statuss = models.BooleanField(default=False)
    time_create = models.DateTimeField(auto_now_add=True)
    time_finish = models.DateTimeField(blank=True)

    def __str__(self):
        return self.title