from django.contrib import admin
from .models import User, ParkingSpace, ParkingReservation

admin.site.register(User)
admin.site.register(ParkingSpace)
admin.site.register(ParkingReservation)
