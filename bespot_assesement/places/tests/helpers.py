import factory

from bespot_assesement.places.tests.factories import PlaceFactory


def create_place_dataset(count=5):
    """
    Create a dataset of factory-generated Place instances.

    Args:
        count (int): The number of Place instances to create in the dataset.

    Returns:
        list: A list of created Place instances.
    """
    place_dataset = []
    for _ in range(count):
        place = PlaceFactory.build()
        place_dataset.append(place)
        place.save()
    return place_dataset
