import uuid

from django.db import models

class Location(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()

class Place(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    address = models.CharField(max_length=255)
    code = models.CharField(max_length=10)
    location = models.OneToOneField(Location, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    reward_checkin_points = models.IntegerField()
    tags = models.ManyToManyField('Tag')
    type = models.CharField(max_length=20)

class Tag(models.Model):
    name = models.CharField(max_length=20)