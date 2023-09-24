import factory
from faker import Faker

from bespot_assesement.places.models import Place

fake = Faker()


class PlaceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Place

    uuid = factory.Faker("uuid4")  # Generate a random UUID
    address = factory.Faker("address")
    code = factory.Faker("text", max_nb_chars=10)
    location = None  # You can customize this if needed
    name = factory.Faker("word")
    reward_checkin_points = factory.Faker("random_int", min=0, max=1000)
    tags = factory.Faker("words", nb=3)  # Generate a list of random words
    type = factory.Faker("word")

    @classmethod
    def create_with_location(cls, location):
        # Create a Place with a specific location
        return cls(location=location)
