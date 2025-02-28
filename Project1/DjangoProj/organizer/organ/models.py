from django.db import models


class Tasks(models.Model):
    userID = models.IntegerField(blank=False)
    title = models.CharField(max_length=25, default="Название задачи")
    descriptionn = models.CharField(blank=False, max_length=255, default="Описание задачи")
    statuss = models.BooleanField(default=False)
    time_create = models.DateTimeField(auto_now_add=True)
    time_finish = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title