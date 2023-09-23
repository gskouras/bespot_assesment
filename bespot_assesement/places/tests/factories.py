import factory
from django.contrib.auth.models import User
from faker import Faker

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username: str = factory.LazyAttribute(lambda _: fake.name())
    email: str = factory.LazyAttribute(lambda _: fake.email())
