from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Q
from django.views.generic.detail import DetailView


# Create your views here.

def home(request):
    amenities_objs = Amenities.objects.all()
    hotels_objs = Hotel.objects.all()

    sort_by = request.GET.get('sort_by')
    search = request.GET.get('search')
    amenities = request.GET.getlist('amenities')
    checkin = request.GET.get('checkin')
    checkout = request.GET.get('checkout')

    if sort_by:
        if sort_by == 'asc':
            hotels_objs = hotels_objs.order_by('-hotel_price')
        elif sort_by == 'dsc':
            hotels_objs = hotels_objs.order_by('hotel_price')

    if search:
        hotels_objs = hotels_objs.filter(
            Q(hotel_name__icontains=search) |
            Q(description__icontains=search)
        )

    if checkin and checkout:
        unavailable_hotels = HotelBooking.objects.filter(
            Q(check_in__lt=checkout, check_out__gt=checkin)
        ).values_list('hotel', flat=True)
        hotels_objs = hotels_objs.exclude(id__in=unavailable_hotels)

    if len(amenities):
        hotels_objs = hotels_objs.filter(amenities__amenity_name__in=amenities).distinct()

    context = {
        'amenities_objs': amenities_objs,
        'hotels_objs': hotels_objs,
        'sort_by': sort_by,
        'search': search,
        'amenities': amenities,
        'checkin': checkin,
        'checkout': checkout
    }

    return render(request, 'home.html', context)

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username)

        if not user_obj.exists():
            messages.warning(request, "Account not found")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        user_obj = authenticate(username = username, password = password)
        if not user_obj:
            messages.warning(request, 'invalid password')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        login(request, user_obj)
        return redirect('/')

    return render(request, 'login.html')

def register_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username)

        if user_obj.exists():
            messages.warning(request, "Username already exists")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        user = User.objects.create(username = username)
        user.set_password(password)
        user.save()

        messages.success(request, "Registration successful. You can now log in.")
        return redirect('/')

    return render(request, 'register.html')

def hotel_detail(request):
    amenities_objs = Amenities.objects.all()
    hotels_objs = Hotel.objects.all()

    sort_by = request.GET.get('sort_by')
    search = request.GET.get('search')
    amenities = request.GET.getlist('amenities')
    print(amenities)
    if sort_by:
        if sort_by == 'asc':
            hotels_objs = hotels_objs.order_by('-hotel_price')
        elif sort_by == 'dsc':
            hotels_objs = hotels_objs.order_by('hotel_price')

    if search:
        hotels_objs = hotels_objs.filter
        Q(hotel_name__icontains = search)
        Q(description__icontains = search)

    if len(amenities):
        hotels_objs = hotels_objs.filter(amenities__amenity_name__in = amenities).distinct()

    context = {'amenities_objs' : amenities_objs, 'hotels_objs' : hotels_objs, 'sort_by': sort_by, 'search' : search, 'amenities' : amenities}

    return render(request, 'hoteldetail.html')

class HotelDetailView(DetailView):
    model = Hotel
    template_name = 'hoteldetail.html'
    context_object_name = 'hotel'

    def get_object(self):
        uid = self.kwargs['uid']
        return Hotel.objects.get(uid=uid)
    
@login_required
def book_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, uid=hotel_id)  # Use uid for lookup
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.hotel = hotel
            booking.save()
            messages.success(request, "Booking successful!")
            return redirect('hotel_detail', uid=hotel_id)
    else:
        form = BookingForm()
    return render(request, 'book_hotel.html', {'form': form, 'hotel': hotel})