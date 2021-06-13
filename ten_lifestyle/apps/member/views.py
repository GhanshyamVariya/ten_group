import csv
import io
from datetime import datetime

from rest_framework import generics, status, mixins, viewsets, filters as search_filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from ten_lifestyle.apps.member.models import Members
from ten_lifestyle.apps.member.serializers import FileUploadSerializer, MembersSerializer


class AddMembersAPIView(generics.CreateAPIView):
    serializer_class = FileUploadSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        decoded_file = file.read().decode()
        io_string = io.StringIO(decoded_file)
        reader = csv.reader(io_string)
        member_objs = [
            Members(
                name=row[0],
                surname=row[1],
                booking_count=row[2],
                created_at=datetime.strptime(row[3], '%d/%m/%y %H:%M')
            )
            for row in reader
        ]
        Members.objects.bulk_create(member_objs, ignore_conflicts=True)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MembersViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    filter_backends = (search_filters.SearchFilter, search_filters.OrderingFilter)
    search_fields = ['id', 'name', 'surname', ]
    serializer_class = MembersSerializer
    pagination_class = LimitOffsetPagination
    ordering_fields = ['id', 'name', 'surname', 'created_at']
    queryset = Members.objects.all().order_by('-created_at')
