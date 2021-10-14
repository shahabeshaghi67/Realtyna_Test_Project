from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from rest_framework import generics
from listing.models import ListingOwner, Room, Reservation
from django.db.models.query_utils import Q
from listing.serializers import ListingOwnerSerializer, RoomCheckSerializer, RoomSerializer, ReservationSerializer
from rest_framework import status
from rest_framework.response import Response


class ListingOwnerView(generics.CreateAPIView,
                       generics.ListAPIView):
    serializer_class = ListingOwnerSerializer
    queryset = ListingOwner.objects.all()


class RoomView(generics.CreateAPIView,
               generics.ListAPIView):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    

class ReservationView(generics.CreateAPIView,
                      generics.ListAPIView):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()


class MyReservationsView(ListView):
    template_name = 'my_reservations.html'

    def get_queryset(self):
        listing_owner_name = self.kwargs.get('listing_owner_name')
        listing_owner = get_object_or_404(ListingOwner, name=listing_owner_name)
        return Reservation.objects.filter(room__listing_owner=listing_owner)


class CheckReservationView(generics.GenericAPIView):
    serializer_class = RoomCheckSerializer
    queryset = Reservation.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        rooms_num = serializer.validated_data['rooms_num']
        date = serializer.validated_data['date']
        listing_owner = serializer.validated_data['listing_owner']
        available_rooms = Room.objects.filter(listing_owner=listing_owner) \
                                      .exclude(Q(reservations__start__lt=date) and\
                                               Q(reservations__end__gt=date)) \
                                      .count()
        data = {
            'is_available' : rooms_num <= available_rooms,
        }
        return Response(data, status=status.HTTP_200_OK)