from rest_framework import serializers
from .models import ListingOwner, Reservation, Room


class ListingOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingOwner
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

    def validate(self, data):
        if data['start'] >= data['end']:
            raise serializers.ValidationError("finish must occur after start")

        # time check
        room = data['room']
        start = data['start']
        end = data['end']
        can_reserve = Reservation.check_new_reservation(room, start, end)
        if not can_reserve:
            raise serializers.ValidationError(
                "the room is reserved at this time!")
        return data


class RoomCheckSerializer(serializers.Serializer):
    listing_owner = serializers.PrimaryKeyRelatedField(
        queryset=ListingOwner.objects.all(), write_only=True)
    rooms_num = serializers.IntegerField(write_only=True)
    date = serializers.DateTimeField(write_only=True)
