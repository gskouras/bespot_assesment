from typing import Type

from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import GenericViewSet

from bespot_assesement.places.api.serializers import (
    PlaceReadSerializer,
    PlaceSerializer,
)
from bespot_assesement.places.api.viewsets.mixins import (
    DestroyByUUIDMixin,
    UpdatebyUUIDMixin,
)
from bespot_assesement.places.models import Place


class PlaceViewSet(
    ListModelMixin,
    CreateModelMixin,
    UpdatebyUUIDMixin,
    DestroyByUUIDMixin,
    GenericViewSet,
):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def get_serializer_class(self) -> Type[BaseSerializer]:
        if self.action in ["list", "update"]:
            return PlaceReadSerializer
        return PlaceSerializer
