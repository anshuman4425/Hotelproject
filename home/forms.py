from django import forms
from .models import HotelBooking

class BookingForm(forms.ModelForm):
    class Meta:
        model = HotelBooking
        fields = ['check_in', 'check_out']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
        }
