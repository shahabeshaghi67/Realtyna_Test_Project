from django.db import models
from django.db.models.query_utils import Q


class ListingOwner(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    listing_owner = models.ForeignKey(ListingOwner, null=False,
                                      on_delete=models.CASCADE)
    number = models.CharField(max_length=255, null=False)

    def __str__(self):
        return f'{self.listing_owner}-{self.number}'

    class Meta:
        unique_together = ('listing_owner', 'number')


class Reservation(models.Model):
    name = models.CharField(max_length=255, null=False)
    room = models.ForeignKey(Room, null=False, on_delete=models.CASCADE,
                             related_name='reservations')
    start = models.DateTimeField(null=False)
    end = models.DateTimeField(null=False)

    def __str__(self):
        return f'{self.name}-{self.start}-{self.end}'

    @staticmethod
    def check_new_reservation(room, start, end):
        room_reservations_count = Reservation.objects.filter(room=room) \
                                             .filter(((Q(end__gt=start) and \
                                                       Q(end__lte=end)) or\
                                                      (Q(start__gte=start) and \
                                                       Q(start__lt=end)) or \
                                                      (Q(start__lte=start) and \
                                                       Q(end__gte=end)))) \
                                             .count()
        if room_reservations_count > 0:
            return False
        return True