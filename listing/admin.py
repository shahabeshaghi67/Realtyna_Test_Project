from django.contrib import admin
from .models import ListingOwner, Room, Reservation


admin.site.register(ListingOwner)
admin.site.register(Room)
admin.site.register(Reservation)
