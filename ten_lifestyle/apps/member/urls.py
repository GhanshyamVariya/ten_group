from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ten_lifestyle.apps.member.views import AddMembersAPIView, MembersViewSet

router = DefaultRouter()
router.register('members-list', MembersViewSet, basename='members_list')

urlpatterns = [
    path('', include(router.urls)),
    path('upload-data', AddMembersAPIView.as_view(), name='dashboard-data'),
]
