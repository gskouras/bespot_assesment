from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers

from  bespot_assesement.places.models import Place, Location, Tag

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('lat', 'lon')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)

class PlaceSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Place
        exclude = ('id',) 

    def create(self, validated_data):
        location_data = validated_data.pop('location')
        tags_data = validated_data.pop('tags')

        # Create or update the Location instance
        location, _ = Location.objects.get_or_create(**location_data)

        # Create or update the Tag instances
        tags = [Tag.objects.get_or_create(name=tag_data['name'])[0] for tag_data in tags_data]

        # Create the Place instance
        place = Place.objects.create(location=location, **validated_data)

        # Add tags to the office
        place.tags.add(*tags)

        return place

    def to_representation(self, instance):
        print(f'\location tags are {instance.location}\n')
        print(f'\ninstance tags are {instance.__dict__}\n')
        representation = super().to_representation(instance)    
        # Replace the 'location' field with its string representation
        # representation['tags'] = instance.tags.name

        return representation