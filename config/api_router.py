from rest_framework.routers import DefaultRouter

from bespot_assesement.places.api.viewsets import PlaceViewSet

router = DefaultRouter()

router.register("place", PlaceViewSet)

app_name = "api"

urlpatterns = router.urls
