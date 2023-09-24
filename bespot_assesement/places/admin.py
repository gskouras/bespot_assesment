from django.contrib import admin

from bespot_assesement.places.models import Place


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "address")
    list_filter = ("name", "address")  # Add a filter option for location
    search_fields = ("name", "address")  # Enable search by name and location
    ordering = ("-name",)  # Default ordering by creation date
