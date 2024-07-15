from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Hotel)

admin.site.register(models.Amenities)

admin.site.register(models.HotelBooking)

admin.site.register(models.HotelImages)