import csv
import io
from datetime import datetime

from rest_framework import generics, status, mixins, filters as search_filters, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from ten_lifestyle.apps.inventory.models import Inventory
from ten_lifestyle.apps.inventory.serializers import InventorySerializer
from ten_lifestyle.apps.member.serializers import FileUploadSerializer


class AddInventoryAPIView(generics.CreateAPIView):
    serializer_class = FileUploadSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        decoded_file = file.read().decode()
        io_string = io.StringIO(decoded_file)
        reader = csv.reader(io_string)
        inventory_objs = [
            Inventory(
                title=row[0],
                description=row[1],
                remaining_count=row[2],
                expiration_date=datetime.strptime(row[3], '%d/%m/%y')
            )
            for row in reader
        ]
        Inventory.objects.bulk_create(inventory_objs, ignore_conflicts=True)
        return Response(status=status.HTTP_204_NO_CONTENT)


class InventoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    filter_backends = (search_filters.SearchFilter, search_filters.OrderingFilter)
    search_fields = ['id', 'title', 'description', ]
    serializer_class = InventorySerializer
    pagination_class = LimitOffsetPagination
    ordering_fields = ['id', 'title', 'description', 'remaining_count', 'expiration_date', 'created_at']
    queryset = Inventory.objects.all().order_by('-created_at')
