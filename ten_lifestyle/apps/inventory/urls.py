from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ten_lifestyle.apps.inventory.views import InventoryViewSet, AddInventoryAPIView

router = DefaultRouter()
router.register('inventory-list', InventoryViewSet, basename='inventory_list')

urlpatterns = [
    path('', include(router.urls)),
    path('upload-data', AddInventoryAPIView.as_view(), name='inventory-data'),
]
