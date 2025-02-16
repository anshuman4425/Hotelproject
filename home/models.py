from django.db import models
from django.contrib.auth.models import User
from statistics import mode
import uuid
from django import forms

# Create your models here.
class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

class Amenities(BaseModel):
    amenity_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.amenity_name

class Hotel(BaseModel):
    hotel_name=models.CharField(max_length=100)
    hotel_price = models.IntegerField()
    description = models.TextField() 
    amenities = models.ManyToManyField(Amenities)  
    room_count = models.IntegerField(default=10)


    def __str__(self) -> str:
        return self.hotel_name

class HotelImages(BaseModel):
    hotel=models.ForeignKey(Hotel, related_name = "Images", on_delete=models.CASCADE)
    Images = models.ImageField(upload_to="hotel")

class HotelBooking(BaseModel):
    hotel= models.ForeignKey(Hotel, related_name = "hotel_booking", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_booking', on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    booking_type = models.CharField(choices=(('Pre Paid', 'Pre Paid'), ('Post Paid', 'Post Paid')), max_length=10)

class BookingForm(forms.ModelForm):
    class Meta:
        model = HotelBooking
        fields = ['check_in', 'check_out', 'booking_type']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
        }
