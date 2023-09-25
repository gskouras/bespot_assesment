from django.core.cache import cache
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response


class CreateClearedChachedModelMixin(CreateModelMixin):
    def create(self, request, *args, **kwargs):
        cache_key = "places_list"
        cache.delete(cache_key)

        return super().create(request, *args, **kwargs)


class UpdatebyUUIDMixin(UpdateModelMixin):

    lookup_field = "uuid"

    def update(self, request, *args, **kwargs):
        cache_key = "places_list"
        cache.delete(cache_key)

        return super().update(request, *args, **kwargs)


class DestroyByUUIDMixin(DestroyModelMixin):

    lookup_field = "uuid"

    def destroy(self, request, *args, **kwargs):
        # Clear the cache when a new object is created
        cache_key = "places_list"
        cache.delete(cache_key)

        return super().destroy(request, *args, **kwargs)
