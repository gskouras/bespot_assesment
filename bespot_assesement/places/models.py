import uuid

from django.db import models


class Location(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self) -> str:
        return f"{self.lat}, {self.lon}"


class Place(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    address = models.CharField(max_length=255)
    code = models.CharField(max_length=10)
    location = models.OneToOneField(
        Location, on_delete=models.CASCADE, blank=True, null=True
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    reward_checkin_points = models.IntegerField(blank=True, null=True)
    tags = models.JSONField(blank=True, null=True)
    type = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name
