import pytest
from rest_framework.test import APITestCase

from bespot_assesement.places.api.serializers import (
    PlaceReadSerializer,
    PlaceSerializer,
)
from bespot_assesement.places.api.viewsets import PlaceViewSet
from bespot_assesement.places.models import Location, Place
from bespot_assesement.places.tests.helpers import create_place_dataset


class PlacesAPITestCase(APITestCase):
    viewset = PlaceViewSet

    @classmethod
    def setUpClass(cls) -> None:
        super(PlacesAPITestCase, cls).setUpClass()
        cls.dataset = create_place_dataset()
        cls.viewset = PlaceViewSet()

    @pytest.fixture(autouse=True)
    def configure_settings(self, settings):
        # The `settings` argument is a fixture provided by pytest-django.
        settings.CACHES = {
            "default": {
                "BACKEND": "django.core.cache.backends.dummy.DummyCache"
            }
        }

    def test_list_places(self):
        response = self.client.get("/api/v1/place/")
        self.assertEqual(len(response.data), 5)

    def test_list_places_search_name(self):
        address = self.dataset[1].address
        response = self.client.get(f"/api/v1/place/?search={address}")
        self.assertEqual(len(response.data), 1)

    def test_create_place_without_loaction(self):
        # Create a sample Place instance with a location via API
        place_data = {
            "address": "123 Main St",
            "code": "ABC123",
            "name": "Sample Place",
            "reward_checkin_points": 10,
            "tags": ["tag1", "tag2"],
            "type": "Restaurant",
        }

        place_response = self.client.post(
            "/api/v1/place/", place_data, format="json"
        )
        self.assertEqual(place_response.status_code, 201)
        place_uuid = place_response.data["uuid"]

        # Retrieve the created Place and Location objects from the database
        place = Place.objects.filter(uuid=place_uuid).first()

        # Check if the Place and Location were created correctly
        self.assertEqual(place.address, "123 Main St")

    def test_create_place_with_loaction(self):
        # Create a sample Place instance with a location via API
        place_data = {
            "address": "123 Main St",
            "code": "ABC123",
            "name": "Sample Place",
            "reward_checkin_points": 10,
            "tags": ["tag1", "tag2"],
            "location": {"lat": 37.978693, "lon": 23.712884},
            "type": "Restaurant",
        }

        place_response = self.client.post(
            "/api/v1/place/", place_data, format="json"
        )
        self.assertEqual(place_response.status_code, 201)
        place_uuid = place_response.data["uuid"]

        # Retrieve the created Place and Location objects from the database
        place = Place.objects.filter(uuid=place_uuid).first()

        # Check if the Place and Location were created correctly
        self.assertEqual(place.address, "123 Main St")

    def test_get_serializer_class(self):
        view = PlaceViewSet()
        view.action = "list"
        self.assertEqual(view.get_serializer_class(), PlaceReadSerializer)

        view.action = "create"
        self.assertEqual(view.get_serializer_class(), PlaceSerializer)
