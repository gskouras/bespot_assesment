# type: ignore
from rest_framework import serializers

from bespot_assesement.places.models import Location, Place


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ("lat", "lon")


class PlaceSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = Place
        exclude = ("id",)

    def create(self, validated_data):
        location_data = validated_data.pop("location")
        # Create or update the Location instance
        location, _ = Location.objects.get_or_create(**location_data)

        # Create the Place instance
        place = Place.objects.create(location=location, **validated_data)

        return place


class PlaceReadSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)

    class Meta:
        model = Place
        exclude = ("id",)
