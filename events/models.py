import datetime
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


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def validate_phone_number(self):
        if self.phone_number and not self.phone_number.isdigit():
            raise ValueError('Phone number must contain only digits.')
        if self.phone_number and len(self.phone_number) != 11:
            raise ValueError('Phone number must be 11 digits long.')

    def validate_date_of_birth(self):
        if self.date_of_birth and self.date_of_birth > datetime.date.today():
            raise ValueError('Date of birth cannot be in the future.')

    def save(self, *args, **kwargs):
        self.validate_phone_number()
        self.validate_date_of_birth()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return self.user.username
