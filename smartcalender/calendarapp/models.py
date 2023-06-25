from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Scheduler(models.Model):
    event_name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.event_name
    
    def duration(self):
        return self.end_date - self.start_date


# class Analytics(models.Model):
#     date = models.DateField()
#     duration = models.DurationField()
#     scheduler = models.ForeignKey(Scheduler, on_delete=models.CASCADE)