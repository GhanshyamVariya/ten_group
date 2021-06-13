from django.db.models import F
from rest_framework import mixins, viewsets, filters as search_filters, status
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from ten_lifestyle.apps.booking.models import Bookings
from ten_lifestyle.apps.booking.serializers import BookingsSerializer, CreateBookSerializer, CancelBookSerializer
from ten_lifestyle.apps.inventory.models import Inventory
from ten_lifestyle.apps.member.models import Members
from ten_lifestyle.settings import MAX_BOOKINGS


class BookingsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    filter_backends = (search_filters.SearchFilter, search_filters.OrderingFilter)
    search_fields = ['id', 'member__name', 'member__surname', 'inventory__title', 'inventory__description']
    serializer_class = BookingsSerializer
    pagination_class = LimitOffsetPagination
    ordering_fields = ['id', 'member__name', 'member__surname', 'inventory__title', 'inventory__description',
                       'created_at']
    queryset = Bookings.objects.select_related('member', 'inventory').order_by('-created_at')


class BookingView(GenericAPIView):

    def post(self, request):
        try:
            serializer = CreateBookSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {"message": "Something went wrong.!!", "error": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            member_id = serializer.validated_data.get('member_id')
            inventory_id = serializer.validated_data.get('inventory_id')

            member_count = Bookings.objects.filter(member_id=member_id).count()
            if member_count < MAX_BOOKINGS:
                inventory_info = Inventory.objects.get(id=inventory_id)
                inventory_count = Bookings.objects.filter(inventory_id=inventory_id).count()

                if inventory_info.remaining_count > inventory_count:
                    Members.objects.filter(id=member_id).update(booking_count=F('booking_count') + 1)
                    Bookings.objects.create(
                        member_id=member_id, inventory_id=inventory_id
                    )
                    inventory_info.remaining_count = inventory_info.remaining_count - 1
                    inventory_info.save()

                    return Response({"message": "Booking is accepted"}, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {"message": "Inventory no longer has capacity.!!"},
                        status=status.HTTP_200_OK,
                    )
            else:
                return Response(
                    {"message": "This member has crossed maximum count of booking.!"},
                    status=status.HTTP_200_OK,
                )

        except Inventory.DoesNotExist:
            return Response(
                {"message": 'Invalid request. Inventory not found'},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Members.DoesNotExist:
            return Response(
                {"message": 'Invalid request. Member not found'},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as ex:
            return Response(
                {"message": "Internal server error", "error": str(ex)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CancelView(GenericAPIView):

    def post(self, request):
        try:
            serializer = CancelBookSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {"message": "Something went wrong.!!", "error": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            book_id = serializer.validated_data.get('book_id')

            book_info = Bookings.objects.get(id=book_id)

            Members.objects.filter(id=book_info.member.id).update(booking_count=F('booking_count') - 1)
            Inventory.objects.filter(id=book_info.inventory.id).update(remaining_count=F('remaining_count') + 1)

            book_info.delete()
            return Response({"message": "Booking is canceled"}, status=status.HTTP_200_OK)

        except Bookings.DoesNotExist:
            return Response(
                {"message": 'Invalid request. Booking not found'},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as ex:
            return Response(
                {"message": "Internal server error", "error": str(ex)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
