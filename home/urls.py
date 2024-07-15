from .views import *
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', home, name="home"),
    path('login/', login_page, name='login_page'),
    path('hotel/<uuid:uid>/', HotelDetailView.as_view(), name='hotel_detail'),
    path('register/', register_page, name='register_page'),
    path('booking/', hotel_detail, name='booking'),
    path('book/<uuid:hotel_id>/', book_hotel, name='book_hotel')  # Use uuid instead of int
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    
urlpatterns += staticfiles_urlpatterns()