from django.core.cache import cache
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response


class ListCachedModelMixin(ListModelMixin):
    def list(self, request, *args, **kwargs):
        cache_key = "places_list"

        # Attempt to get the data from cache
        cached_data = cache.get(cache_key)
        print(cached_data)
        if cached_data:
            # If data is found in cache, return it
            return Response(cached_data)

        cache.set(cache_key, request.data, 3600)
        return super().list(request, *args, **kwargs)


class CreateClearedChachedModelMixin(CreateModelMixin):
    def create(self, request, *args, **kwargs):
        # Clear the cache when a new object is created
        cache_key = "places_list"
        cache.delete(cache_key)

        return super().create(request, *args, **kwargs)


class UpdatebyUUIDMixin(UpdateModelMixin):

    lookup_field = "uuid"


class DestroyByUUIDMixin(DestroyModelMixin):

    lookup_field = "uuid"
