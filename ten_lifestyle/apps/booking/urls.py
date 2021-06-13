from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ten_lifestyle.apps.booking.views import BookingsViewSet, BookingView, CancelView

router = DefaultRouter()
router.register('booking-list', BookingsViewSet, basename='booking_list')

urlpatterns = [
    path('', include(router.urls)),
    path('book', BookingView.as_view(), name='book_create'),
    path('cancel', CancelView.as_view(), name='cancel_booking'),
]
