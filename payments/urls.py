from rest_framework import routers

from . import api

router = routers.DefaultRouter()
router.register(r'payments', api.PaymentsViewSet, 'payments')

urlpatterns = router.urls