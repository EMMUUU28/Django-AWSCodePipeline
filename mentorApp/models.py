from django.db import models

class Meeting(models.Model):
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    roomName = models.CharField(max_length=255)
    roomUrl = models.URLField(max_length=200)
    meetingId = models.CharField(max_length=255)
    hostname = models.CharField(max_length=255)
    objective = models.TextField()

    def __str__(self):
        return self.roomName