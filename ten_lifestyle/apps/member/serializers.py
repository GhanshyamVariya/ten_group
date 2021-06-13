from rest_framework import serializers

from ten_lifestyle.apps.member.models import Members


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class MembersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Members
        fields = '__all__'
