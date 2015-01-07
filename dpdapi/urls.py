from rest_framework.routers import DefaultRouter

from .views import AliasViewSet, DomainViewSet, UserViewSet


router = DefaultRouter()
router.register(r'aliases', AliasViewSet)
router.register(r'domains', DomainViewSet)
router.register(r'users', UserViewSet)
urlpatterns = router.urls