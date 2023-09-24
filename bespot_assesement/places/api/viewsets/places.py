from typing import Type

from django.core.cache import cache
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import GenericViewSet

from bespot_assesement.places.api.serializers import (
    PlaceReadSerializer,
    PlaceSerializer,
)
from bespot_assesement.places.api.viewsets.mixins import (
    CreateClearedChachedModelMixin,
    DestroyByUUIDMixin,
    UpdatebyUUIDMixin,
)
from bespot_assesement.places.models import Place


class PlaceViewSet(
    CreateClearedChachedModelMixin,
    UpdatebyUUIDMixin,
    DestroyByUUIDMixin,
    GenericViewSet,
):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    filterset_fields = ["name", "address", "uuid"]
    ordering_fields = ["name", "address", "uuid"]
    ordering = ["address", "name"]
    filter_backends = (OrderingFilter, SearchFilter)
    search_fields = ["name", "address"]

    def list(self, request: Request, *args, **kwargs):
        # Define a cache key specific to this view
        cache_key = "places_list"
        # Attempt to get the data from cache
        cached_data = cache.get(cache_key)

        if cached_data and dict(request.query_params) == {}:
            return Response(cached_data)

        # If data is not in cache, execute the query
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        # Store the query result in cache for future use
        cache.set(cache_key, serializer.data, 3600)  # Cache for 1 hour
        return Response(serializer.data)

    def get_serializer_class(self) -> Type[BaseSerializer]:
        if self.action in ["list", "update"]:
            return PlaceReadSerializer
        return PlaceSerializer
