from django.urls import path
from .views import ListingOwnerView, MyReservationsView, CheckReservationView, ReservationView, RoomView


urlpatterns = [
    path('reservation/', ReservationView.as_view(), name='reservation'),
    path('listing-owner/', ListingOwnerView.as_view(), name='listing-owner'),
    path('room/', RoomView.as_view(), name='room'),
    path('my-reservations/<str:listing_owner_name>/',
         MyReservationsView.as_view(), name='my-reservations'),
    path('check/', CheckReservationView.as_view(), name='check-reservation'),
]
