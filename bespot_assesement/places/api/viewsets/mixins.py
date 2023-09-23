from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin


class UpdatebyUUIDMixin(UpdateModelMixin):
    """
    A mixin that retrieves a model instance by UUID instead of the default ID.
    """

    lookup_field = "uuid"


class DestroyByUUIDMixin(DestroyModelMixin):

    lookup_field = "uuid"
