from django.urls import path, re_path

from . import views     # it means - 'from all import views'
from .views import hotel,booking,cancellation,deleteReservation,allBookings,manageBooking,editBooking,saveEdits
urlpatterns = [
    path('',hotel, name='index'),
    path('booking',booking,name='booking'),
    path('cancellation',cancellation,name='cancellation'),
    path('cancellation/<str:id>/', deleteReservation, name='deleteReservation'),
    path('bookingHistory',allBookings,name='allBookings'),
    path('manageBooking',manageBooking,name='manageBooking'),
    path('editBooking',editBooking,name='editBooking'),
    path('manageBooking',saveEdits,name="saveEdits")
]