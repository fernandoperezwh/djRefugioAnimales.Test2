from rest_framework import routers

from src.apps.mascota.api.views.view_set import VacunaViewSet, MascotaViewSet

router = routers.SimpleRouter()
router.register(r'vacunas', VacunaViewSet)
router.register(r'mascotas', MascotaViewSet)

urlpatterns = []

urlpatterns += router.urls
