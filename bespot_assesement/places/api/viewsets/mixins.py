from rest_framework.generics import RetrieveAPIView
from django.shortcuts import get_object_or_404
from django.http import Http404

class RetrieveByUUIDMixin:
    """
    A mixin that retrieves a model instance by UUID instead of the default ID.
    """
    lookup_field = 'uuid'

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj