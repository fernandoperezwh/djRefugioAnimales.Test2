from rest_framework import routers

from src.apps.adopcion.api.views.view_set import PersonaViewSet

router = routers.SimpleRouter()
router.register(r'personas', PersonaViewSet)

urlpatterns = []

urlpatterns += router.urls
