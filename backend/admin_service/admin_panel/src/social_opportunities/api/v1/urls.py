from rest_framework.routers import DefaultRouter

from .views import (
    CompanyViewSet,
    ContactsViewSet,
    ServiceViewSet,
    UsedServiceViewSet,
    СlickedServiceViewSet,
    NotUsedServiceViewSet,
    CooperationViewSet,
    ApplicationViewSet,
)

router = DefaultRouter()
router.register(r"services", ServiceViewSet)
router.register(r"companies", CompanyViewSet)
router.register(r"contacts", ContactsViewSet)
router.register(r"used_service/clicked", СlickedServiceViewSet)
router.register(r"used_service/not_used", NotUsedServiceViewSet)
router.register(r"used_service", UsedServiceViewSet)
router.register(r"cooperation", CooperationViewSet)
router.register(r"application", ApplicationViewSet)

urlpatterns = router.urls
