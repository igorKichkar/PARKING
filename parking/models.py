from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    status = models.BooleanField(default=False, verbose_name='Manager')

    def __str__(self):
        if self.is_staff:
            return 'Admin: {} {}'.format(self.first_name, self.last_name)
        else:
            if self.status:
                status = 'Manager'
            else:
                status = 'Employee'
        return '{} {} ({})'.format(self.first_name, self.last_name, status)


class ParkingSpace(models.Model):
    number = models.CharField(max_length=255, unique=True, verbose_name='Parking space number')

    def __str__(self):
        return self.number


class ParkingReservation(models.Model):
    parking_number = models.ForeignKey(ParkingSpace, on_delete=models.CASCADE)
    data = models.DateField(verbose_name='Booking date')
    start_time = models.TimeField(verbose_name='Start of Booking Time')
    end_time = models.TimeField(verbose_name='End of Booking Time')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Employee')

    def __str__(self):
        return 'Reserved time {} - {}'.format(self.start_time, self.end_time)

    class Meta:
        ordering = ('parking_number', 'data', 'start_time')
