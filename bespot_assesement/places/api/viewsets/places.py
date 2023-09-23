from typing import Type

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet

from bespot_assesement.places.api.serializers import (
    PlaceSerializer,
)
from bespot_assesement.places.models import Place
from bespot_assesement.places.api.viewsets.mixins import RetrieveByUUIDMixin

class PlaceViewSet(
    RetrieveByUUIDMixin,
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        tags = request.data.get("tags", [])
        request.data["tags"] =[{"name": tag} for tag in tags]

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    