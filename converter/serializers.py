from rest_framework import serializers
from .models import Conversion


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    target_format = serializers.CharField(max_length=10)


class ConversionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversion
        fields = '__all__'
