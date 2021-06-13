from rest_framework import serializers

from ten_lifestyle.apps.booking.models import Bookings


class BookingsSerializer(serializers.ModelSerializer):
    member_name = serializers.ReadOnlyField(source='member.name', read_only=True)
    member_surname = serializers.ReadOnlyField(source='member.surname', read_only=True)
    inventory_title = serializers.ReadOnlyField(source='inventory.title', read_only=True)
    inventory_description = serializers.ReadOnlyField(source='inventory.description', read_only=True)

    class Meta:
        model = Bookings
        fields = '__all__'


class CreateBookSerializer(serializers.Serializer):
    member_id = serializers.IntegerField(required=True)
    inventory_id = serializers.IntegerField(required=True)


class CancelBookSerializer(serializers.Serializer):
    book_id = serializers.IntegerField(required=True)
