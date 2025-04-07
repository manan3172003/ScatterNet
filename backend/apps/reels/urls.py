from rest_framework.routers import DefaultRouter
from .views import ReelViewSet
router = DefaultRouter()
router.register(r'reels', ReelViewSet)
urlpatterns = router.urls