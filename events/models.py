from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Event(models.Model):
    CATEGORY_CHOICES = (
        ('music', 'Music'),
        ('theatre', 'Theatre'),
        ('festival', 'Festival'),
        ('conference', 'Conference'),
        ('concert', 'Concert'),
        ('workshop', 'Workshop'),
        ('exhibition', 'Exhibition'),
        ('other', 'Other'),
    )
    name = models.CharField(max_length=255)
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    capacity = models.PositiveIntegerField(default=100)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} booked {self.event.name}"
